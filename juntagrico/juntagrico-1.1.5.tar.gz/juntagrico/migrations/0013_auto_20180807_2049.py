# Generated by Django 2.0.2 on 2018-08-07 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0012_auto_20180509_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionsize',
            name='units',
            field=models.PositiveIntegerField(unique=True, verbose_name='Einheiten'),
        ),
    ]
