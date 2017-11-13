# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-11-04 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0013_auto_20171103_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark_attendance', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], max_length=50)),
                ('date', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='date',
        ),
        migrations.RemoveField(
            model_name='student',
            name='mark_attendance',
        ),
        migrations.AddField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Student'),
        ),
    ]