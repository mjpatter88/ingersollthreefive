# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-22 01:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=100)),
                ('comments', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
