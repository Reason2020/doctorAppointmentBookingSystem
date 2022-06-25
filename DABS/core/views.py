#render & redirect imports
from django.shortcuts import render, redirect
#necessary import for generating pdf
from django.http import FileResponse, HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


#models, decorators, filters and forms imports
from .models import *
from .decorators import unauthenticated_user, allowed_users, admin_only
from .filters import AppointmentsFilter, DoctorsFilter
from .forms import DoctorForm, AppointmentForm, PatientAppointmentForm, RegisterNewUserForm, AccountSettingsForm

#login and authentication imports
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#default groups imports
from django.contrib.auth.models import Group

# Create your views here.


#Register Patient View
@unauthenticated_user
def registrationPageView(request):
    form = RegisterNewUserForm()

    if request.method == 'POST':
        form = RegisterNewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='patient')
            user.groups.add(group)

            Patient.objects.create(
                user=user,
            )

            username = form.cleaned_data.get('username')
            messages.success(request, 'Account Created Successfully for ' + username)
            return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'core/register.html', context)


#Login Page View
@unauthenticated_user
def loginPageView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin')
        else:
            messages.info(request, 'Invalid Username or Password')
    context = {

    }
    return render(request, 'core/login.html', context)


#Logout View
def logoutUser(request):
    logout(request)
    return redirect('login')


#First Page Of the System
def homePageView(request):
    return render(request, 'core/home.html')


#Admin Home Page View
@login_required(login_url='login')
@admin_only
def adminPageView(request):
    appointments = Appointment.objects.all()
    appointments_count = appointments.count()
    appointments_completed = appointments.filter(status = "Checked").count()
    appointments_pending = appointments.filter(status="Pending").count()
    context = {
        'appointments': appointments,
        'appointments_count': appointments_count,
        'appointments_completed': appointments_completed,
        'appointments_pending': appointments_pending,
    }
    return render(request, 'core/adminsHome.html', context)


#Patients Home Page View
@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def userPageView(request):
    doctors = Doctor.objects.all()

    doctorFilter = DoctorsFilter(request.GET, queryset=doctors)
    doctors = doctorFilter.qs

    context = {
        'doctors': doctors,
        'doctorFilter': doctorFilter,
    }
    return render(request, 'core/usersHome.html', context)


#Accounts Settings View
@login_required
@allowed_users(allowed_roles=['patient'])
def accountSettings(request):
    patient = request.user.patient
    form = AccountSettingsForm(instance=patient)

    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'core/account_settings.html', context)


#Appointments List for patient
@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def patientAppointmentsListPageView(request):
    appointments = request.user.patient.appointment_set.all()

    appointmentFilter = AppointmentsFilter(request.GET, queryset=appointments)
    appointments = appointmentFilter.qs

    context = {
        'appointments': appointments,
        'appointmentFilter': appointmentFilter,
    }
    return render(request, 'core/patientAppointmentsList.html', context)


#Doctors Home Page
@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def doctorPageView(request):
    appointments = request.user.doctor.appointment_set.all()
    print('APPOINTMENTS:', appointments)

    context = {
        'appointments': appointments
    }
    return render(request, 'core/doctorsHome.html')


#DOctors List View for admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def doctorsListPageView(request):
    doctors = Doctor.objects.all()
    doctors_count = doctors.count()
    md_doctors = doctors.filter(degree="MD").count()
    do_doctors = doctors.filter(degree="DO").count()
    context = {
        'doctors': doctors,
        'doctors_count': doctors_count,
        'md_doctors': md_doctors,
        'do_doctors': do_doctors,
    }
    return render(request, 'core/doctorsList.html', context)


#Patients List View For admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def patientsListPageView(request):
    patients = Patient.objects.all()
    patient_count = patients.count()
    male_patient = patients.filter(gender="Male").count()
    female_patient = patients.filter(gender="Female").count()
    context = {
        'patients': patients,
        'patient_count': patient_count,
        'male_patient': male_patient,
        'female_patient': female_patient,
    }
    return render(request, 'core/patientsList.html', context)


#Register DOctor View for admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def doctorRegistrationFormView(request):
    form = RegisterNewUserForm()

    if request.method == 'POST':
        form = RegisterNewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='doctor')
            user.groups.add(group)

            Doctor.objects.create(
                user=user
            )
            return redirect('doctorsList')
        # else:
        #     return HttpResponse('Booyahhhhhh!')

    context = {
        'form': form,
    }
    return render(request, 'core/doctorRegistrationForm.html', context)


#Update Doctor View For admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def doctorUpdationFormView(request, pk):
    selected_doctor = Doctor.objects.get(id=pk)
    form = DoctorForm(instance=selected_doctor)

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=selected_doctor)
        if form.is_valid:
            form.save()
            return redirect('doctorsList')
        else:
            return redirect('doctorsList')

    context = {
        'form': form,
    }
    return render(request, 'core/doctorUpdationForm.html', context)


#Delete Doctor View for admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def doctorDeletionFormView(request, pk):
    selected_doctor = Doctor.objects.get(id=pk)
    # form = AdminCRUDConfirmationForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            selected_doctor.delete()
            return redirect('doctorsList')
        else:
            messages.info(request, 'Sorry, Login Credentials Incorrect. Cannot Perform Deletion')


    context = {
        'selected_doctor': selected_doctor,
        # 'form': form,
    }
    return render(request, 'core/doctorDeletionForm.html', context)


#Make Appointment View
@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def makeAppointmentFormView(request, pk):
    patient = request.user.patient
    doctor = Doctor.objects.get(id=pk)
    form = PatientAppointmentForm(initial={'patient': patient, 'doctor': doctor})

    if request.method == "POST":
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user')
    context = {
        'form': form,
    }
    return render(request, 'core/makeAppointmentForm.html', context)


#Update Appointment View for patient
@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def myAppointmentUpdateFormView(request, pk):
    appointment = Appointment.objects.get(id=pk)
    form = PatientAppointmentForm(instance=appointment)

    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('myAppointments')
    context = {
        'form': form,
    }
    return render(request, 'core/myAppointmentUpdateForm.html', context)


#Delete Appointment view for patient
@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def myAppointmentDeleteFormView(request, pk):
    appointment = Appointment.objects.get(id=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('myAppointments')
    context = {
        'appointment': appointment,
    }
    return render(request, 'core/myAppointmentDeleteForm.html', context)


#Update Appointment View for admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def appointmentUpdateFormView(request, pk):
    selected_appointment = Appointment.objects.get(id=pk)
    form = AppointmentForm(instance=selected_appointment)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=selected_appointment)
        form.save()
        return redirect('admin')

    context = {
        'form': form,
    }
    return render(request, 'core/appointmentUpdateForm.html', context)


#Delete appointment view for admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def appointmentDeleteFormView(request, pk):
    selected_appointment = Appointment.objects.get(id=pk)

    if request.method == 'POST':
        selected_appointment.delete()
        return redirect('admin')

    context = {
        'selected_appointment': selected_appointment
    }
    return render(request, 'core/appointmentDeleteForm.html', context)


#Generate appointment pdf
def appointment_pdf(request, pk):
    #Create Bytestream buffer
    buf = io.BytesIO()

    #Create Canvas
    canv = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    #Create a text object
    textObj = canv.beginText()
    textObj.setTextOrigin(inch, inch)
    textObj.setFont("Helvetica", 14)

    #Get the appointment
    appointment = Appointment.objects.get(id=pk)

    #blank list
    lines = []

    #Append lines to list
    lines.append('Doctor: {doctorFirstName} {doctorLastName}'.format(doctorFirstName=appointment.doctor.first_name, doctorLastName=appointment.doctor.last_name))
    lines.append('Patient: {patientFirstName} {patientLastName}'.format(patientFirstName=appointment.patient.first_name, patientLastName=appointment.patient.last_name))
    lines.append('Reason of appointment: {appointmentReason}'.format(appointmentReason=appointment.reason))
    lines.append('Date of Appointment: {appointmentDate}'.format(appointmentDate=appointment.date))
    lines.append('Appointment Time: {appointmentTime}'.format(appointmentTime=appointment.time))
    lines.append('Appointment Status: {appointmentStatus}'.format(appointmentStatus=appointment.status))

    #loop
    for line in lines:
        textObj.textLine(line)

    #FInish Up
    canv.drawText(textObj)
    canv.showPage()
    canv.save()
    buf.seek(0)

    #Return
    return FileResponse(buf, as_attachment=True, filename="appointment.pdf")
