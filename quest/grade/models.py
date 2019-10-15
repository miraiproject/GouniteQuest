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

class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username 