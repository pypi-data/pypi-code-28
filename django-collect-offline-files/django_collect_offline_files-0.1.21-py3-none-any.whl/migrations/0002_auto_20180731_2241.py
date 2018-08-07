# Generated by Django 2.0.7 on 2018-07-31 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_collect_offline_files', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='exportedtransactionfilehistory',
            name='django_offl_created_2b049a_idx',
        ),
        migrations.RemoveIndex(
            model_name='exportedtransactionfilehistory',
            name='django_offl_sent_da_e863ed_idx',
        ),
        migrations.AddIndex(
            model_name='exportedtransactionfilehistory',
            index=models.Index(fields=['created'], name='django_coll_created_908dd1_idx'),
        ),
        migrations.AddIndex(
            model_name='exportedtransactionfilehistory',
            index=models.Index(fields=['sent_datetime'], name='django_coll_sent_da_c80fee_idx'),
        ),
    ]
