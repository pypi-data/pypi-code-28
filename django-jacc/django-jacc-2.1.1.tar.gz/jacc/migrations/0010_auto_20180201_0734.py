# Generated by Django 2.0.1 on 2018-02-01 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jacc', '0009_accountentry_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttype',
            name='is_asset',
            field=models.BooleanField(verbose_name='asset'),
        ),
    ]
