# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-22 05:26
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mallard_qr', '0001_squashed_0005_fix_concept_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrationmode',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid1, editable=False, help_text='Universally-unique Identifier. Uses UUID1 as this improves uniqueness and tracking between registries', unique=True),
        ),
    ]
