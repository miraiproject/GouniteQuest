from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import GradeForm
from .models import Grade, CustomUser
from django.db.models import Avg


def new_grade(request, user_id):
    if not request.user.is_teacher:
        return redirect("grade:index")
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.user = user
            grade.gpa = (grade.english + grade.math + grade.japanese) / 3
            grade.save()
            messages.success(request, "成績を保存しました")
            return redirect("grade:show_grade")
    else:
        form = GradeForm()
    return render(request, "grade/new_grade.html",
                  {"form": form, "user": user})


def update_grade(request, user_id):
    if not request.user.is_teacher:
        return redirect("grade:index")
    user = get_object_or_404(CustomUser, id=user_id)
    grade = get_object_or_404(Grade, user=user)
    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.gpa = (grade.english + grade.math + grade.japanese) / 3
            grade.save()
            messages.success(request, "成績を保存しました")
            return redirect("grade:show_grade")
    else:
        form = GradeForm(instance=grade)
    return render(request, "grade/update_grade.html",
                  {"form": form, "user": user})


def show_grade(request):
    if not request.user.is_teacher:
        return redirect("grade:index")
    students = CustomUser.objects.filter(is_teacher=False)
    avg_english = Grade.objects.aggregate(Avg('english'))
    avg_math = Grade.objects.aggregate(Avg('math'))
    avg_japanese = Grade.objects.aggregate(Avg('japanese'))
    return render(request, "grade/show_grade.html",
                  {"students": students,
                   "avg_english": avg_english["english__avg"],
                   "avg_math": avg_math["math__avg"],
                   "avg_japanese": avg_japanese["japanese__avg"]})
