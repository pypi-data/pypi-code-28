# Generated by Django 2.0.1 on 2018-01-23 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('edc_lab', '0014_auto_20180123_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='manifestitem',
            name='site',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='sites.Site'),
        ),
    ]
