# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-07 12:43
from __future__ import unicode_literals

from django.db import migrations
import edc_model_fields.fields.uuid_auto_field


class Migration(migrations.Migration):

    dependencies = [
        ('edc_identifier', '0003_auto_20160625_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identifiertracker',
            name='id',
            field=edc_model_fields.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subjectidentifier',
            name='id',
            field=edc_model_fields.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
    ]
