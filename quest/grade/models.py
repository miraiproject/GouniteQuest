from django.contrib.auth.models import User
from django.db import models
import os


class Grade(models.Model):
    english = models.IntegerField()
    math = models.IntegerField()
    japanese = models.IntegerField()
    gpa = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class ReportProblem(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Report(models.Model):
    report_file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    report_problem = models.ForeignKey(ReportProblem, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.username


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


def get_upload_to(instance, filename):
    return os.path.join(str(instance.teacher), filename)


class Profile(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    # image = models.FileField(upload_to='uploads/%Y/%m/%d/')
    image = models.ImageField(upload_to=get_upload_to)
    introduction = models.TextField(max_length=400)

    def __str__(self):
        return self.introduction
