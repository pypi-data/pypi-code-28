# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-11 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_ffmpeg', '0003_add_thumb_conv_cmd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Title'),
        ),
    ]
