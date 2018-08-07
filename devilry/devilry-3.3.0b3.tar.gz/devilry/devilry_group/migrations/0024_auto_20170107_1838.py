# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-07 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devilry_group', '0023_auto_20170104_0551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackset',
            name='feedbackset_type',
            field=models.CharField(choices=[('first_attempt', 'first attempt'), ('new_attempt', 'new attempt'), ('re_edit', 're edit')], db_index=True, default='new_attempt', max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='feedbackset',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='feedbackset',
            name='is_last_in_group',
        ),
    ]
