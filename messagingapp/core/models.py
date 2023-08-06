from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

# implementing custom user model for future extending ability (much harder to implement after first migration)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)