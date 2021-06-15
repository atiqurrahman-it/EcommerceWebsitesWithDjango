from django.db import models

# to create a custom User model and admin panel (Start)
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_lazy

# To automatically create one ot on objects
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class MyCustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self._create_user(email, password, **extra_fields)


# Create User model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, null=False)
    is_staff = models.BooleanField(ugettext_lazy('staff status'), default=False,
                                   help_text=ugettext_lazy('Designates whether the user can log in this site'))
    is_active = models.BooleanField(ugettext_lazy('active'), default=True,
                                    help_text='Designates whether this user should be treated as active. Unselect '
                                              'this instead of deleting accounts')
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    objects = MyCustomUserManager()

    def __str__(self):
        return self.email

    # optional
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


# to create a custom User model and admin panel (End)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=250, blank=True)
    full_name = models.CharField(max_length=250, blank=True)
    address_1 = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + "'s profile"

    # automatically filleup model filleds when create user
    def profile_is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        for fields_name in fields_names:
            value = getattr(self, fields_name)
            if value is None or value == '':
                return False
        return True

# auto profile mode a object create hobe  when user register korbe 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()  # profile model er related_name
