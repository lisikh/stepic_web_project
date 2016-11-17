
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True)
    rating = models.IntegerField()
    author = models.TextField()
    likes = models.TextField
    def __unicode__(self):
        return self.title

class Answer(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True)
    question = models.TextField()
    author = models.TextField()

user = User()
print(user.get_full_name())