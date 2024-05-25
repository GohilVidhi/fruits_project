# Generated by Django 5.0 on 2024-02-06 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_remove_addcart_coupon_delete_coupon'),
    ]

    operations = [
        migrations.CreateModel(
            name='coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('discount_amount', models.IntegerField()),
                ('min_order_amount', models.IntegerField()),
                ('max_order_amount', models.IntegerField()),
                ('expiry_date', models.DateTimeField()),
            ],
        ),
    ]