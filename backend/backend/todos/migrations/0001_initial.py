# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]