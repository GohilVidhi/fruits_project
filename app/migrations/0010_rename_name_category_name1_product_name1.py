# Generated by Django 5.0 on 2023-12-25 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='name1',
        ),
        migrations.AddField(
            model_name='product',
            name='name1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.category'),
        ),
    ]
