# Generated by Django 2.1.1 on 2018-10-17 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20181017_1219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ('-course_name',)},
        ),
        migrations.AlterModelOptions(
            name='ugrc_topic',
            options={'ordering': ('-ugrc',)},
        ),
    ]
