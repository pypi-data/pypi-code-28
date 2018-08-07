# Generated by Django 2.0.1 on 2018-03-18 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='title model help_text', max_length=255, unique=True)),
                ('body', models.TextField(help_text='article model help_text', max_length=5000)),
                ('slug', models.SlugField(blank=True, help_text='slug model help_text', unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('article_type', models.PositiveSmallIntegerField(choices=[(1, 'first'), (2, 'second'), (3, 'third'), (7, 'seven'), (8, 'eight')], help_text='IntegerField declared on model with choices=(...) and exposed via ModelSerializer', null=True)),
                ('cover', models.ImageField(blank=True, upload_to='article/original/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(help_text='title model help_text', max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, help_text='slug model help_text', unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='group',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, related_name='articles_as_main', to='articles.ArticleGroup'),
        ),
        migrations.AddField(
            model_name='article',
            name='original_group',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, related_name='articles_as_original', to='articles.ArticleGroup'),
        ),
    ]
