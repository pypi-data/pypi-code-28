# Generated by Django 2.0b1 on 2017-10-31 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, help_text="user's country of origin", max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='study_country',
            field=models.CharField(blank=True, help_text="user's country of work", max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='study_site',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
