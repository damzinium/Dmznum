# Generated by Django 2.1.3 on 2018-11-07 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20181017_1237'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ugrc_topic',
            options={'ordering': ('ugrc',)},
        ),
    ]
