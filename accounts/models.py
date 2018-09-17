from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

LEVEL_CHOICES = (
    ("100","100"),
    ("200","200"),
    ("300","300"),
    ("400","400")
    )

class Profile(models.Model):
    from library.models import Institution, Department

    profile_picture = models.ImageField(null=True, blank=True)
    institution = models.ForeignKey(Institution, null=True, on_delete=models.CASCADE)
    department_name = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    level = models.IntegerField(choices=LEVEL_CHOICES)
    phone_number = models.CharField(max_length=10, null=True)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return self.user.username


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)

    profile = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE)

    date_joined = models.DateTimeField(default=timezone.now)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(verbose_name='account status', default=True)
    is_staff = models.BooleanField(verbose_name='staff status', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.first_name.capitalize()

    def get_full_name(self):
        return self.first_name.capitalize() + ' ' + self.last_name.capitalize()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile()
        profile.save()
        instance.profile = profile
        instance.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
