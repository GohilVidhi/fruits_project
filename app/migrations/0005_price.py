# Generated by Django 5.0 on 2023-12-23 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_sub_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price1', models.CharField(max_length=50)),
            ],
        ),
    ]
