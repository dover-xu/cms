# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-10 07:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('focus', '0010_auto_20161210_1519'),
    ]

    operations = [
        migrations.AlterField(
                model_name='tread',
                name='user',
                field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE,
                                        to=settings.AUTH_USER_MODEL),
        ),
    ]
