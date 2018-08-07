# Generated by Django 2.0.2 on 2018-05-09 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0011_auto_20180225_1206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Zahlung', 'verbose_name_plural': 'Zahlungen'},
        ),
        migrations.RenameField('subscriptionsize','size','units'),
        migrations.AlterField(
            model_name='jobextratype',
            name='display_empty',
            field=models.CharField(max_length=1000, verbose_name='Icon für fehlendes Extra'),
        ),
    ]
