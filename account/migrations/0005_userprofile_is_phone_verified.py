# Generated by Django 5.0.4 on 2024-06-11 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_userprofile_otp_code_userprofile_otp_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_phone_verified',
            field=models.BooleanField(default=False),
        ),
    ]
