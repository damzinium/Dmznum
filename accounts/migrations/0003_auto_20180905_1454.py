# Generated by Django 2.1.1 on 2018-09-05 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180905_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile'),
        ),
    ]
