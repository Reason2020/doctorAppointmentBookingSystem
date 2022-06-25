from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePageView, name="home"),
    path('user/', views.userPageView, name="user"),
    path('myAppointments/', views.patientAppointmentsListPageView, name="myAppointments"),
    path('admin/', views.adminPageView, name="admin"),
    path('doctor/', views.doctorPageView, name="doctor"),
    path('login/', views.loginPageView, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registrationPageView, name="registration"),
    path('doctorsList/', views.doctorsListPageView, name="doctorsList"),
    path('patientsList/', views.patientsListPageView, name="patientsList"),
    path('doctorRegistration/', views.doctorRegistrationFormView, name="doctorRegistration"),
    path('doctorUpdation/<int:pk>/', views.doctorUpdationFormView, name="doctorUpdate"),
    path('doctorDeletion/<int:pk>/', views.doctorDeletionFormView, name="doctorDelete"),
    path('makeAppointment/<int:pk>/', views.makeAppointmentFormView, name="makeAppointment"),
    path('updateMyAppointment/<int:pk>/', views.myAppointmentUpdateFormView, name="updateMyAppointment"),
    path('deleteMyAppointment/<int:pk>/', views.myAppointmentDeleteFormView, name="deleteMyAppointment"),
    path('appointmentUpdate/<int:pk>/', views.appointmentUpdateFormView, name="appointmentUpdate"),
    path('appointmentDelete/<int:pk>/', views.appointmentDeleteFormView, name="appointmentDelete"),
    path('appointment_pdf<int:pk>', views.appointment_pdf, name="appointment_pdf"),
    path('account/', views.accountSettings, name="account"),
]
