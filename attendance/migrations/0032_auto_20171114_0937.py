# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-11-14 04:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0031_auto_20171114_0935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='absent',
        ),
        migrations.RemoveField(
            model_name='student',
            name='present',
        ),
        migrations.RemoveField(
            model_name='student',
            name='student_teacher',
        ),
    ]