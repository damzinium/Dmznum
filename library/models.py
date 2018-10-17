from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils import timezone

class Institution(models.Model):
    institution = models.CharField(max_length=100, default="Legon")

    class Meta:
        ordering = ('institution',)

    def __str__(self):
        return self.institution


class School(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100)

    class Meta:
        ordering = ('school_name',)

    def __str__(self):
        return self.school_name


class Department(models.Model):
    school_name = models.ForeignKey(School, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ('department_name',)
       
    def __str__(self):
        return self.department_name


class Course(models.Model):
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)

    class Meta:
        ordering = ('course_name',)
        
    def __str__(self):
        return self.course_code + ":" + self.course_name


class Topic(models.Model):
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField('content')

    class Meta:
        ordering = ('-course_name',)
        
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