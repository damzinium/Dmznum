from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from library.models import School, Department


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_name = models.ForeignKey(School, on_delete=models.CASCADE)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, null=False, blank=False)
    date_of_birth = models.DateField(null=True, blank=False, help_text='MM/DD/YYYY')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        user.save()
        profile = Profile(user=user)
