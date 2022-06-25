from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Patient(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    MARITAL_STATUS = (
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=200, choices=GENDER)
    address = models.CharField(max_length=1000)
    phone = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=100, choices=MARITAL_STATUS)
    added_date = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(default="user.png",null=True, blank=True)

    def __str__(self):
        return  self.user.username

class Shift(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    DEGREE = (
        ('MD', 'MD'),
        ('DO', 'DO'),
    )
    SPECIALTY = (
        ('Pediatrician', 'Pediatrician'),
        ('Allergist', 'Allergists'),
        ('Dermatologist', 'Dermatologist'),
        ('Ophthalmologist', 'Ophthalmologist'),
        ('OB/GYN', 'OB/GYN'),
        ('Cardiologist', 'Cariologist'),
        ('Urologist', 'Urologist'),
        ('Neurologist', 'Neurologist'),
        ('Psychiatrist', 'Psychiatrist'),
    )
    AVAILABILITY = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=1000)
    dob = models.DateField(null=True)
    degree = models.CharField(max_length=200, choices=DEGREE)
    specialty = models.CharField(max_length=200, choices = SPECIALTY)
    availability = models.CharField(max_length=200, choices=AVAILABILITY, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    shift = models.ManyToManyField(Shift)

    def __str__(self):
        return self.first_name

class Appointment(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Checked', 'Checked'),
    )
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.SET_NULL)
    reason = models.TextField(null=True, blank=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    status = models.CharField(max_length=200, choices=STATUS, null=True)

    def __str__(self):
        return self.reason
