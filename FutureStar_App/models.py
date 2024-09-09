from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Role Model
class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# User Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    card_header=models.ImageField(upload_to='card_header/', null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

# System Settings Model
class SystemSettings(models.Model):
    fav_icon = models.CharField(max_length=255, null=True, blank=True)
    footer_logo = models.CharField(max_length=255, null=True, blank=True)
    header_logo = models.CharField(max_length=255, null=True, blank=True)
    website_name_english = models.CharField(max_length=255)
    website_name_arabic = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    instagram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    snapchat = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.website_name_english







############################################################# Models for visualizations ############################################################# 


# gender Model
class UserGender(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Game Type  Model
class GameType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Field Capacity  Model
class FieldCapacity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Ground Materials Model
class GroundMaterial(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Tournamebt Style Model
class TournamentStyle(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Event Types Model
class EventType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name