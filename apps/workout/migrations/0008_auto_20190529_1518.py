# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2019-05-29 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0007_auto_20190528_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='workout',
            name='name_of_workout',
            field=models.CharField(max_length=255),
        ),
    ]