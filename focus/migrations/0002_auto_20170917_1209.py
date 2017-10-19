# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-17 04:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('focus', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='owner',
        ),
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='notes',
                                    to=settings.AUTH_USER_MODEL, verbose_name='who public'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments',
                                    to='focus.Note'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='comments',
                                    to=settings.AUTH_USER_MODEL, verbose_name='who comment'),
        ),
        migrations.AlterField(
            model_name='praise',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='praises',
                                    to=settings.AUTH_USER_MODEL, verbose_name='who praise'),
        ),
        migrations.AlterField(
            model_name='share',
            name='note',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='focus.Note'),
        ),
        migrations.AlterField(
            model_name='share',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='shares',
                                    to=settings.AUTH_USER_MODEL, verbose_name='who share'),
        ),
        migrations.AlterField(
            model_name='tread',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='treads',
                                    to=settings.AUTH_USER_MODEL, verbose_name='who tread'),
        ),
    ]