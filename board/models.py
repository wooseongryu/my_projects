from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    dt_created = models.DateField(auto_now_add=True)
    dt_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
