from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Track(TimeStampedModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Question(TimeStampedModel):
    question = models.CharField('Question', max_length=255)
    idTrack = models.ForeignKey(Track, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class Choice(TimeStampedModel):
    idQuestion = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)

