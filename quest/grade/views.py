from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from grade.forms import BoardForm, GradeForm, ReportForm, ReportProblemForm,ProfileForm,CustomUserCreationForm
from grade.models import Board, Grade, Report, ReportProblem,Profile,CustomUser
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
import django_filters
from rest_framework import viewsets, filters
from .models import Board
from .serializers import BoardSerializer


@login_required
def index(request):
    report_problems = ReportProblem.objects.all()
    photos = Profile.objects.all()
    if request.user.teacher:
        reports = Report.objects.all()
        return render(request, "grade/teacher_home.html",
                      {'report_problems': report_problems,
                       'reports': reports,
                       'photos': photos})
    else:
        grade = Grade.objects.filter(user=request.user).first()
        return render(request, "grade/student_home.html",
                      {'report_problems': report_problems,
                       'grade': grade,
                       'photos': photos})


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
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
        form = CustomUserCreationForm()
    return render(request, "grade/signup.html", {"form": form})


def new_grade(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
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


def update_grade(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    grade = get_object_or_404(Grade, user=user)
    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.gpa = (grade.english + grade.math + grade.japanese) / 3
            grade.save()
            messages.success(request, "成績を保存しました")
            return redirect("grade:index")
    else:
        form = GradeForm(instance=grade)
    return render(request, "grade/update_grade.html",
                  {"form": form, "user": user})


def show_grade(request):
    students = CustomUser.objects.filter(teacher=False)
    avg_english = Grade.objects.aggregate(Avg('english'))
    avg_math = Grade.objects.aggregate(Avg('math'))
    avg_japanese = Grade.objects.aggregate(Avg('japanese'))
    return render(request, "grade/show_grade.html",
                  {"students": students,
                   "avg_english": avg_english["english__avg"],
                   "avg_math": avg_math["math__avg"],
                   "avg_japanese": avg_japanese["japanese__avg"]})


def new_report_problem(request):
    if request.method == "POST":
        form = ReportProblemForm(request.POST)
        if form.is_valid():
            report_problem = form.save(commit=False)
            report_problem.teacher = request.user
            report_problem.save()
            messages.success(request, "レポート課題を作成しました")
            return redirect("grade:index")
    else:
        form = ReportProblemForm()
    return render(request, "grade/new_report_problem.html", {"form": form})


def new_report(request, report_problem_id):
    report_problem = get_object_or_404(ReportProblem, id=report_problem_id)
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.report_problem = report_problem
            report.student = request.user
            report.save()
            messages.success(request, "レポートを提出しました")
            return redirect("grade:index")
    else:
        form = ReportForm()
    return render(request, "grade/new_report.html", {"report_problem": report_problem, "form": form})


def new_board(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            boards = Board.objects.all()
            topic.save()
            messages.success(request, "コメントを追加しました。")
            return redirect("grade:new_board")
    else:
        form = BoardForm()
        boards = Board.objects.all()
    return render(request, "grade/new_board.html", {"form": form, "boards": boards})


def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if board.user == request.user:
        board.delete()

    return redirect("grade:new_board")


def new_profile(request):
    photos = Profile.objects.all()
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.teacher = request.user
            profile.save()
            return redirect("grade:index")
    else:
        form = ProfileForm()
    return render(request, "grade/new_profile.html", {"form": form, "photos": photos})


def update_profile(request):
    profileUser = get_object_or_404(Profile, teacher=request.user)
    photos = Profile.objects.all()
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profileUser)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.teacher = request.user
            profile.save()
            return redirect("grade:index")
    else:
        form = ProfileForm(instance=profileUser)
    return render(request, "grade/update_profile.html", {"form": form, "photos": photos})


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer