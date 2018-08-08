# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-19 11:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UUIDFood',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UUIDTag',
            fields=[
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UUIDTaggedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField(db_index=True, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests_uuidtaggeditem_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests_uuidtaggeditem_items', to='tests.UUIDTag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='uuidfood',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='tests.UUIDTaggedItem', to='tests.UUIDTag', verbose_name='Tags'),
        ),
    ]
