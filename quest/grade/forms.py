from django import forms
from django.forms import ModelForm
from .models import Board, Grade, Report, ReportProblem, Profile, CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ["english", "math", "japanese"]


class ReportProblemForm(ModelForm):
    deadline = forms.DateTimeField(
       label='締め切り',
       required=True,
       widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
       input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = ReportProblem
        fields = ["title", "content", "deadline"]


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["report_file"]


class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['comment']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'introduction']


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'is_teacher')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'is_teacher')
