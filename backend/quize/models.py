from django.db import models
from course.models import Course

# Create your models here.


class Quize(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizes')

    def __str__(self):
        return self.title


class Question(models.Model):
    question = models.CharField(max_length=200)
    quize = models.ForeignKey(Quize, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.question


class Choice(models.Model):
    title = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='question_answer')
    choice = models.OneToOneField(Choice, on_delete=models.CASCADE, related_name='answer')

    def __str__(self):
        return self.choice.title


