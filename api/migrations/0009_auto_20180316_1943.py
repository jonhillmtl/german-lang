# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-16 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20180316_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appsession',
            name='finished_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
