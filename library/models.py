from os import environ

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone


class Institution(models.Model):
    name = models.CharField(max_length=100, default="Legon")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class School(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Department(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Course(models.Model):
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    is_required = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.code + ":" + self.name


class Topic(models.Model):
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

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        limit_choices_to={'is_approved': True}
    )
    replier = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField()
    date_uploaded = models.DateTimeField(editable=False, default=timezone.now)


class Ugrc(models.Model):
    # from accounts.models import Profile

    ugrc = models.CharField(max_length=200)
    ugrc_code = models.CharField(max_length=20)
    # level = models.ForeignKey(Profile, on_delete=models.CASCADE, to_field="level")

    class Meta:
        ordering = ('ugrc',)

    def __str__(self):
        return self.ugrc_code + ":" + self.ugrc

    def get_absolute_url(self):
        return reverse('accounts:ugrc_detail', args=[str(self.id)])


class Ugrc_Topic(models.Model):
    ugrc = models.ForeignKey(Ugrc, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = RichTextUploadingField()

    class Meta:
        ordering = ('ugrc',)

    def get_absolute_url(self):
        return reverse('accounts:profile')

    def __str__(self):
        return self.title


class CourseSelection(models.Model):
    from accounts.models import User

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=((1, 2, ), ), default=environ.get('SEMESTER', 1))
    selection_date = models.DateTimeField(auto_now_add=True)


@receiver(models.signals.post_save, sender=Topic)
def push_updates(sender, instance, **kwargs):
    if instance.push_updates:
        instance.active_content = instance.content
        instance.push_updates = False
        instance.save()
