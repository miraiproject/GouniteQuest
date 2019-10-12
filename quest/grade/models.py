from django.contrib.auth.models import User
from django.db import models


class Grade(models.Model):
    english = models.IntegerField()
    math = models.IntegerField()
    japanese = models.IntegerField()
    gpa = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
