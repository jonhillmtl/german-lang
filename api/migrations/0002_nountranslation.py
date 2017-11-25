# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NounTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=128)),
                ('form', models.CharField(choices=[('s', 'singular'), ('p', 'plural')], max_length=1)),
                ('notes', models.TextField(blank=True, null=True)),
                ('language_code', models.CharField(default='en_US', max_length=5)),
                ('noun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Noun')),
            ],
        ),
    ]
