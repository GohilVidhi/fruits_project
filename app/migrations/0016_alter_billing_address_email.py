# Generated by Django 5.0 on 2024-01-20 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_billing_address_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing_address',
            name='email',
            field=models.EmailField(max_length=50),
        ),
    ]
