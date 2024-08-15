# Generated by Django 5.0.4 on 2024-06-04 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_remove_bet_amount_wagered_bet_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='potential_payout',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
