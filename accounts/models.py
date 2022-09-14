from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=60)
    profile_user = models.ImageField(upload_to='profile_user', null=True, blank=True)
    is_author = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):

        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):

        return self.is_admin




class OTPCode(models.Model):
    email = models.CharField(max_length=200)
    code = models.SmallIntegerField()
    expiration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email