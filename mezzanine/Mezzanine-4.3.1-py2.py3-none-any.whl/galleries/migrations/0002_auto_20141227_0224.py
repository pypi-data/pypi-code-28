# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryimage',
            name='_order',
            field=mezzanine.core.fields.OrderField(null=True, verbose_name='Order'),
            preserve_default=True,
        ),
    ]
