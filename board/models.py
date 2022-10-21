from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_length

class Post(models.Model):
    title = models.CharField(max_length=100, validators=[validate_length])
    content = models.TextField()
    dt_created = models.DateField(auto_now_add=True)
    dt_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class User(AbstractUser):
    pass
