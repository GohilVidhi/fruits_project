# Generated by Django 5.0 on 2024-02-07 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_coupon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user_id',
            new_name='user',
        ),
    ]
