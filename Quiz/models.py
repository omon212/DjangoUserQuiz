from django.db import models
from django.conf import settings
import random


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.subject.name} - {self.text[:50]}"


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"


class UserQuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_results")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.subject.name} - {self.score}/{self.total_questions}"