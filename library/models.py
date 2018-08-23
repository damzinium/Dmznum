from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class School(models.Model):
    school_name = models.CharField(max_length=100)

    def __str__(self):
        return self.school_name

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    school_name = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.department_name

class Course(models.Model):
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)

    def __str__(self):
        return self.course_code + ":" + self.course_name

class Topic(models.Model):
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField('content')

    def get_absolute_url(self):
        return reverse('library:department')

    def __str__(self):
        return self.title


class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, editable=False)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date_uploaded = models.DateTimeField(editable=False, default=timezone.now)
    is_approved = models.BooleanField(verbose_name='check to approve', default=False)

    def __str__(self):
        if self.is_approved:
            return '{} commented on {}. (Approved.)'.format(self.commenter, self.topic)
        else:
            return '{} commented on {}. (Pending Approval.)'.format(self.commenter, self.topic)


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        limit_choices_to={'is_approved': True}
    )
    replier = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField()
    date_uploaded = models.DateTimeField(editable=False, default=timezone.now)


class Ugrc(models.Model):
    ugrc = models.CharField(max_length=200)
    ugrc_code = models.CharField(max_length=20)

    def __str__(self):
        return self.ugrc_code + ":" + self.ugrc


class Ugrc_Topic(models.Model):
    ugrc = models.ForeignKey(Ugrc, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = RichTextUploadingField()

    def get_absolute_url(self):
        return reverse('ugrc:ugrc')

    def __str__(self):
        return self.title