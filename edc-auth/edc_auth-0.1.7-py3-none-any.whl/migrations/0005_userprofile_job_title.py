# Generated by Django 2.1 on 2018-08-04 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_auth', '0004_auto_20180804_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='job_title',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
