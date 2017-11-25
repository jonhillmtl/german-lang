# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Noun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('singular_form', models.CharField(max_length=128)),
                ('plural_form', models.CharField(max_length=128)),
                ('language_code', models.CharField(max_length=5)),
                ('gender', models.CharField(choices=[('m', 'masculine'), ('f', 'feminine'), ('n', 'neuter')], max_length=1)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
    ]