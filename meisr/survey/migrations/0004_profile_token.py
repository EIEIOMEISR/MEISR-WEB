# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-07 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_auto_20180407_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='token',
            field=models.CharField(db_index=True, max_length=15, null=True, unique=True, verbose_name='Token'),
        ),
    ]