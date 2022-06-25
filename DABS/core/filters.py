from dataclasses import fields
from pyexpat import model

import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class DoctorsFilter(django_filters.FilterSet):
    class Meta:
        model = Doctor
        fields = '__all__'
        exclude = ['email', 'phone', 'address', 'dob', 'added_date', 'shift']

class AppointmentsFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date', lookup_expr='gte')
    end_date = DateFilter(field_name='date', lookup_expr='lte')
    reason = CharFilter(field_name='reason', lookup_expr='icontains')

    class Meta:
        model = Appointment
        fields = '__all__'
        exclude = ['patient', 'date']
