# Generated by Django 5.0 on 2023-12-23 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('otp', models.IntegerField(default=123)),
            ],
        ),
    ]
