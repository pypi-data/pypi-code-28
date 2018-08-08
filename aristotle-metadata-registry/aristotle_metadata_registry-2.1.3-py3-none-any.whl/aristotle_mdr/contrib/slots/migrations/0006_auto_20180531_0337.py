# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-31 03:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_mdr_slots', '0005_slot_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slot',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='slot',
            name='permission',
            field=models.IntegerField(choices=[(0, 'All'), (1, 'Authenticated'), (2, 'Workgroup')], default=0),
        ),
    ]
