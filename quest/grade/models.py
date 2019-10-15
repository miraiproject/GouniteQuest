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


class Report(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SubmittedReport(models.Model):
    submittion = models.FileField(upload_to='uploads/%Y/%m/%d/')
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.username
