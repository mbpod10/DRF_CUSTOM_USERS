from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    user = models.ForeignKey(User, related_name='books',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)

    def __str__(self):
        return self.title
