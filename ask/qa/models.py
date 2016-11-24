
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


# Create your models here.
class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-id')
    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True,auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    likes = models.ManyToManyField(User, related_name='u')

    def __unicode__(self):
        return self.title
    def get_url(self):
        return reverse('question', kwargs={'question_id': self.id})
    def get_answer(self):
        answers = self.answer_set.all().count()
        return answers


class Answer(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    def __unicode__(self):
        return self.text
    def get_url(self):
        return reverse('question', kwargs={'question_id': self.question_id})

