# Generated by Django 2.0.2 on 2018-02-06 16:02

from django.db import migrations


def migrate_subscriptions(apps, schema_editor):
    Subscription = apps.get_model('juntagrico', 'Subscription')
    for sub in Subscription.objects.all():
        if sub.active is False and sub.deactivation_date is None:
            for member in sub.members.all():
                    member.subscription=None
                    member.future_subscription=sub
                    member.save()
        if sub.active is False and sub.deactivation_date is not None:
            for member in sub.members.all():
                member.old_subscriptions.add(sub)
                member.subscription=None
                member.save()


class Migration(migrations.Migration):
    dependencies = [
        ('juntagrico', '0008_auto_20180130_2321'),
    ]

    operations = [
        migrations.RunPython(migrate_subscriptions),
    ]
