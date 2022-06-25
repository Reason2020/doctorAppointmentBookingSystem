from dataclasses import fields
from pyexpat import model
from tkinter import DISABLED
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

class AccountSettingsForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['user', 'added_date']

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'status']

class PatientAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        exclude = ['status']

class RegisterNewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# class AdminCRUDConfirmationForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
