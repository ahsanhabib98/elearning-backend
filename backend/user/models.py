from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_instructor = models.BooleanField(default=False)
    is_learner = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


def user_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_instructor:
            Instructor.objects.create(user=instance)
        else:
            Learner.objects.create(user=instance)


post_save.connect(user_save_receiver, sender=User)


class Instructor(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='user/instructor_image', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor')
    profile_link = models.TextField(null=True, blank=True)
    journal_link = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.email


class Learner(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    organization_name = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(upload_to='user/learner_image', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learner')

    def __str__(self):
        return self.user.email