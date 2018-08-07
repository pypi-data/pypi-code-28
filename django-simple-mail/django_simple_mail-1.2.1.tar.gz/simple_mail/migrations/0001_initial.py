# Generated by Django 2.1 on 2018-08-07 17:36

from django.db import migrations, models
from simple_mail.settings import sm_settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleMail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20, unique=True, choices=sm_settings.EMAILS, verbose_name='Email Key')),
                ('subject', models.CharField(max_length=255, verbose_name='Subject')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Content')),
                ('button_label', models.CharField(blank=True, max_length=80, verbose_name='Button label')),
                ('button_link', models.CharField(blank=True, max_length=255, verbose_name='Button Link')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
        ),
    ]
