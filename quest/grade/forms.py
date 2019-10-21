from django.forms import ModelForm
from grade.models import Board
from grade.models import Grade
from grade.models import Report
from grade.models import ReportProblem
from grade.models import Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ["english", "math", "japanese"]


class ReportProblemForm(ModelForm):
    class Meta:
        model = ReportProblem
        fields = ["title", "content"]


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
        fields = ('username','teacher')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username','teacher')