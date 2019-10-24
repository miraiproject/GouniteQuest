from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import BoardForm, ProfileForm, CustomUserCreationForm
from .models import Board, Grade, Report, ReportProblem, Profile
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    photos = Profile.objects.all()
    if request.user.is_teacher:
        report_problems = ReportProblem.objects.order_by('deadline')
        reports = Report.objects.order_by('-created_datetime')
        return render(request, "grade/teacher_home.html",
                      {'report_problems': report_problems,
                       'reports': reports,
                       'photos': photos})
    else:
        report_id = Report.objects.values_list(
                        "report_problem_id", flat=True
                    ).filter(student=request.user)
        submitted_problems = ReportProblem.objects.filter(
                                 id__in=report_id
                             ).order_by('deadline')
        not_submitted_problems = ReportProblem.objects.exclude(
                                     id__in=report_id
                                 ).order_by('deadline')
        grade = Grade.objects.filter(user=request.user).first()
        reports = Report.objects.filter(
                      student=request.user
                  ).order_by('-created_datetime')
        return render(request, "grade/student_home.html",
                      {'grade': grade,
                       'reports': reports,
                       'submitted_problems': submitted_problems,
                       'not_submitted_problems': not_submitted_problems,
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
    return render(request, "grade/new_board.html",
                  {"form": form, "boards": boards})


def delete_board(request):
    board = Board.objects.filter(user=request.user)
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
    return render(request, "grade/new_profile.html",
                  {"form": form, "photos": photos})


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
    return render(request, "grade/update_profile.html",
                  {"form": form, "photos": photos})
