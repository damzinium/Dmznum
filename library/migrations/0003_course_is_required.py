# Generated by Django 2.1.1 on 2019-03-23 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20190323_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_required',
            field=models.BooleanField(default=False),
        ),
    ]
