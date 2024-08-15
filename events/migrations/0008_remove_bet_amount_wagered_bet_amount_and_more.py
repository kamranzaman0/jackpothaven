# Generated by Django 5.0.4 on 2024-06-04 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_event_venue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bet',
            name='amount_wagered',
        ),
        migrations.AddField(
            model_name='bet',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='bet',
            name='payment_intent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]