from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
from django.conf import settings
from django.utils import timezone
# https://pypi.org/project/shortuuid/
from shortuuid.django_fields import ShortUUIDField 
# https://django-phonenumber-field.readthedocs.io/en/latest/#
from phonenumber_field.modelfields import PhoneNumberField
# https://docs.python.org/3/library/contextlib.html
import contextlib
import random
import uuid



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email, password, **extra_fields)



# https://github.com/django/django/blob/main/django/contrib/auth/models.py#L334
"""https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#substituting-a-custom-user-model"""
class UserModel(AbstractUser, PermissionsMixin):
    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)                     
    username         = None
    email            = models.EmailField(unique = True,  null = True)
    first_name       = models.CharField(max_length = 50, null = True)
    last_name        = models.CharField(max_length = 50 ,null = True)
    is_verifiedEmail = models.BooleanField(default=False)
    enable_two_factor_authentication = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]
   
    def __str__(self):
       return "{}".format(self.email) 
    
    @property
    def get_user_fullname(self):
        return f"{self.first_name} {self.last_name}"
      
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_verified = True 
            self.enable_two_factor_authentication = False
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'UserModel'
        verbose_name_plural = 'UsersModel'






class UserProfile(models.Model):
    id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    
    bio             = models.TextField(blank=True, null=True)
    profile_image   = models.ImageField(upload_to='user/profile_pictures/', blank=True, null=True)
    date_of_birth   = models.DateField(blank=True, null=True)
    gender          = models.CharField(max_length=10, blank=True, null=True)
    phone_number    = PhoneNumberField(blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at      = models.DateTimeField(auto_now_add=False, auto_now=True)
    address         = models.CharField(max_length=100, blank=True, null=True)
    # city            = models.CharField(max_length=50, blank=True, null=True)
    # state           = models.CharField(max_length=50, blank=True, null=True)
    # country         = models.CharField(max_length=50, blank=True, null=True)
    
    def save(self, *args, **kwargs): 
        # Deletes old profile_picture when making an update to profile_picture
        with contextlib.suppress(Exception):
            old = UserProfile.objects.get(id=self.id)
            if old.profile_picture != self.profile_picture:
                old.profile_picture.delete(save=False)
        
        # Set the userprofile ID to be the same as the user ID
        self.id = self.user.id
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.user.email

    




class SMSCode(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)                     
    user       = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='smscode')
    OTP_code   = models.CharField(max_length=6, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # modify OTP_code_number for each registered user to chech with it later
    def save(self, *args, **kwargs):
        verification_code = random.randint(100000, 999999)
        self.OTP_code = str(verification_code)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user.first_name}-{self.OTP_code}'

    def is_expired(self, expiration_minutes=10):
        expiration_time = self.created_at + timezone.timedelta(minutes=expiration_minutes)
        return timezone.now() >= expiration_time
