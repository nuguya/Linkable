# Generated by Django 2.2.1 on 2019-05-08 14:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_recommend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommend',
            name='books',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=20),
        ),
    ]