import os
import uuid


from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone


class Institution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default="Legon")

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
    institution = models.ForeignKey(Institution, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    @property
    def is_required(self):
        if self.department is not None:
            return False
        return True
        
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.code + ":" + self.name


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    active_content = RichTextUploadingField(editable=False, null=True)
    content = RichTextUploadingField('content')
    push_updates = models.BooleanField(default=False)

    class Meta:
        ordering = ('-title',)

    def get_absolute_url(self):
        return reverse('accounts:profile')

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
        if self.is_approved:
            return '{} commented on {}. (Approved.)'.format(self.commenter, self.topic)
        else:
            return '{} commented on {}. (Pending Approval.)'.format(self.commenter, self.topic)


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


@receiver(models.signals.post_save, sender=Topic)
def push_updates(sender, instance, **kwargs):
    if instance.push_updates:
        instance.active_content = instance.content
        instance.push_updates = False
        instance.save()
