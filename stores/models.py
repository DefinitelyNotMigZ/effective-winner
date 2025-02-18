from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


# Create your models here.

class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

class Stores(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    store_name = models.CharField(max_length=50, null=False, unique=True)
    main_product = models.CharField(max_length=50, null=False)
    floor_location = models.CharField(max_length=10, null=False)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='stores')




