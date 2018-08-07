# Generated by Django 2.0.1 on 2018-03-18 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TodoAnother',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('todo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.Todo')),
            ],
        ),
        migrations.CreateModel(
            name='TodoYetAnother',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('todo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.TodoAnother')),
            ],
        ),
    ]
