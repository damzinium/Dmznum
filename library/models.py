import os
import uuid


from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone


class Institution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution = models.ForeignKey(Institution, null=True, on_delete=models.CASCADE, editable=False)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    is_required = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        if self.department is None:
            self.is_required = True
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.code + ":" + self.name


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    
    prev = models.OneToOneField('self', null=True, blank=True, verbose_name='previous topic', on_delete=models.DO_NOTHING, related_name='next')

    def clean(self):
        if self.prev is None:
            try:
                super(Topic, self).objects.get(course=self.course, prev__isnull=True)
            except:
                raise ValidationError({'prev':'A first topic already exists.'})

    def __str__(self):
        return self.title




class SubTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(editable=False, null=True)
    temp_content = RichTextUploadingField(verbose_name='content')
    push_updates = models.BooleanField(default=False)

    prev = models.OneToOneField('self', null=True, blank=True, verbose_name='previous subtopic', on_delete=models.DO_NOTHING, related_name='next')

    def clean(self):
        if self.prev is None:
            try:
                super().objects.get(topic=self.topic, prev__isnull=True)
            except:
                raise ValidationError({'prev': 'A first sub-topic already exists'})

    def __str__(self):
        return self.title


class Comment(models.Model):
    from accounts.models import User

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, editable=False)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date_uploaded = models.DateTimeField(editable=False, default=timezone.now)
    is_approved = models.BooleanField(verbose_name='check to approve', default=False)

    def __str__(self):
        self.commenter.username


class Reply(models.Model):
    from accounts.models import User

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        limit_choices_to={'is_approved': True}
    )
    replier = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField()
    date_uploaded = models.DateTimeField(editable=False, default=timezone.now)


class CourseSelection(models.Model):
    from accounts.models import User

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=((1, 2, ), ), default=os.environ.get('SEMESTER', 2))
    selection_date = models.DateTimeField(auto_now_add=True)


@receiver(models.signals.post_save, sender=SubTopic)
def push_updates(sender, instance, **kwargs):
    if instance.push_updates:
        instance.content = instance.temp_content
        instance.push_updates = False
        instance.save()
