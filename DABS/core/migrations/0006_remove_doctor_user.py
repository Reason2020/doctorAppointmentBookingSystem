# Generated by Django 4.0.4 on 2022-06-24 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_doctor_user_alter_patient_profile_pic_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='user',
        ),
    ]
