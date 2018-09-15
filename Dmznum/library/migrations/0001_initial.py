# Generated by Django 2.1.1 on 2018-09-14 03:06

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date_uploaded', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_approved', models.BooleanField(default=False, verbose_name='check to approve')),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100)),
                ('course_code', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('course_name',),
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('department_name',),
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('institution',),
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('100', '100'), ('200', '200'), ('300', '300'), ('400', '400')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField()),
                ('date_uploaded', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('comment', models.ForeignKey(limit_choices_to={'is_approved': True}, on_delete=django.db.models.deletion.CASCADE, to='library.Comment')),
                ('replier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=100)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Institution')),
            ],
            options={
                'ordering': ('school_name',),
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='content')),
                ('course_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Course')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Ugrc_100',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ugrc', models.CharField(max_length=200)),
                ('ugrc_code', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('ugrc',),
            },
        ),
        migrations.CreateModel(
            name='Ugrc_200',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ugrc', models.CharField(max_length=200)),
                ('ugrc_code', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('ugrc',),
            },
        ),
        migrations.CreateModel(
            name='Ugrc_Topic_100',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('ugrc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Ugrc_100')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Ugrc_Topic_200',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('ugrc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Ugrc_200')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.AddField(
            model_name='department',
            name='school_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.School'),
        ),
        migrations.AddField(
            model_name='course',
            name='department_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Department'),
        ),
        migrations.AddField(
            model_name='comment',
            name='topic',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='library.Topic'),
        ),
    ]
