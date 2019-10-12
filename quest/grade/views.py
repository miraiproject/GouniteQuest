from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from grade.forms import GradeForm
from grade.models import Grade
from grade.models import User


def index(request):
    users = User.objects.all()
    return render(request, "grade/index.html", {'users': users})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_username = form.cleaned_data["username"]
            input_password = form.cleaned_data["password1"]
            new_user = authenticate(
                username=input_username,
                password=input_password
                )
            if new_user is not None:
                login(request, new_user)
                messages.success(request, "ユーザー登録が完了しました")
                return redirect("grade:index")
    else:
        form = UserCreationForm()
    return render(request, "grade/signup.html", {"form": form})


def new_grade(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.user = user
            grade.gpa = (grade.english + grade.math + grade.japanese) / 3
            grade.save()
            messages.success(request, "成績を保存しました")
            return redirect("grade:index")
    else:
        form = GradeForm()
        return render(request, "grade/new_grade.html",
                      {"form": form, "user": user})
