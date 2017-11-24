# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-24 06:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('focus', '0009_auto_20171124_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='profile',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='profile'),
        ),
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL, verbose_name='who public'),
        ),
    ]
