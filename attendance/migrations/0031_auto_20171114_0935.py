# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-11-14 04:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0030_auto_20171114_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_teacher',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='attendance.Teacher'),
        ),
    ]
