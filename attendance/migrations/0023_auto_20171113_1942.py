# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-11-13 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0022_auto_20171113_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='principal_name',
            field=models.CharField(max_length=500),
        ),
    ]
