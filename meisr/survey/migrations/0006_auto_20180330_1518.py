# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-30 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_auto_20180330_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
