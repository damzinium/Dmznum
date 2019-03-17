# Generated by Django 2.1.1 on 2018-12-16 20:09

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20181107_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='active_content',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='active content empty'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='push_updates',
            field=models.BooleanField(default=True),
        ),
    ]
