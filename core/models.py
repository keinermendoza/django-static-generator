import uuid
from django.db import models
from django.core.files.storage import default_storage
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário deve ter um endereço de e-mail")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário precisa ter is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário precisa ter is_superuser=True")

        return self.create_user(email=email, password=password, **extra_fields)



# https://www.geeksforgeeks.org/imagefield-django-models/
def get_profile_image_path(self, filename): 
    return f'profile_images/{self.id}/profile.jpg'

class CustomUser(AbstractBaseUser, PermissionsMixin):

    # primarykey
    # https://docs.djangoproject.com/en/5.2/ref/models/fields/#uuidfield
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # optionals
    name = models.CharField(max_length=80, blank=True)
    _profile_image = models.ImageField(max_length=300, upload_to=get_profile_image_path, blank=True)

    # required
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(max_length=120, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email" # used by login views and by backend authenticate

    REQUIRED_FIELDS = []
    PATH_TO_DEFAULT_IMAGE = "profile_images/default.jpg"
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj = None) -> bool:
        return self.is_admin

    def has_module_perms(self, app_label) -> bool:
        return self.is_admin

    @property
    def profile_image(self):
        if self._profile_image:
            return self._profile_image.url
        return default_storage.url(self.PATH_TO_DEFAULT_IMAGE)
