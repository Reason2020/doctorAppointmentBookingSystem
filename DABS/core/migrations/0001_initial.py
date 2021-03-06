# Generated by Django 4.0.4 on 2022-05-21 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=200)),
                ('address', models.CharField(max_length=1000)),
                ('phone', models.CharField(max_length=10)),
                ('marital_status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], max_length=100)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=1000)),
                ('dob', models.DateField()),
                ('degree', models.CharField(choices=[('MD', 'MD'), ('DO', 'DO')], max_length=200)),
                ('specialty', models.CharField(choices=[('Pediatrician', 'Pediatrician'), ('Allergist', 'Allergists'), ('Dermatologist', 'Dermatologist'), ('Ophthalmologist', 'Ophthalmologist'), ('OB/GYN', 'OB/GYN'), ('Cardiologist', 'Cariologist'), ('Urologist', 'Urologist'), ('Neurologist', 'Neurologist'), ('Psychiatrist', 'Psychiatrist')], max_length=200)),
                ('availability', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=200, null=True)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('shift', models.ManyToManyField(to='core.shift')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True, null=True)),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Checked', 'Checked')], max_length=200, null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.patient')),
            ],
        ),
    ]
