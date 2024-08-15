# Generated by Django 5.0.4 on 2024-06-04 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_venue_bet_league_result_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.venue'),
        ),
    ]
