from django.db import models
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from .validators import validate_length, validate_no_special_charactors

class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        error_messages={"unique": '해당 닉네임은 이미 사용중입니다!'},
        validators = [validate_no_special_charactors],
    )

    slug = AutoSlugField(
        populate_from='nickname',
        unique=True,
        null=True
    )

    def __str__(self):
        return self.nickname


class Post(models.Model):
    title = models.CharField(max_length=100, validators=[validate_length])
    content = models.TextField()
    dt_created = models.DateField(auto_now_add=True)
    dt_updated = models.DateField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
