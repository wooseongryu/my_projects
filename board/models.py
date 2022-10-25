from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from .validators import validate_length, validate_no_special_charactors

class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        error_messages={"unique": '해당 닉네임은 이미 사용중입니다!'},
        validators = [validate_no_special_charactors],
    )

    slug = models.SlugField(
        unique=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nickname, allow_unicode=True)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.nickname)


class Post(models.Model):
    title = models.CharField(max_length=100, validators=[validate_length])
    content = models.TextField()
    dt_created = models.DateField(auto_now_add=True)
    dt_updated = models.DateField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
