# Generated by Django 2.0b1 on 2017-11-16 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edc_lab', '0008_auto_20170921_0719'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalaliquot',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical '},
        ),
        migrations.AlterModelOptions(
            name='historicalbox',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical '},
        ),
        migrations.AlterModelOptions(
            name='historicalboxitem',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical '},
        ),
        migrations.AlterModelOptions(
            name='historicalconsignee',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical '},
        ),
        migrations.AlterModelOptions(
            name='historicalmanifest',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical '},
        ),
        migrations.AlterModelOptions(
            name='historicalshipper',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical '},
        ),
    ]
