# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-11-13 17:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0028_student_student_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='attendance.Teacher'),
        ),
    ]
