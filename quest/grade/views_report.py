from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ReportForm, ReportProblemForm
from .models import ReportProblem


def new_report_problem(request):
    if not request.user.is_teacher:
        return redirect("grade:index")
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


def update_report_problem(request, report_problem_id):
    report_problem = get_object_or_404(ReportProblem, id=report_problem_id)
    if request.user != report_problem.teacher:
        return redirect("grade:index")
    if request.method == "POST":
        form = ReportProblemForm(request.POST, instance=report_problem)
        if form.is_valid():
            report_problem = form.save(commit=False)
            report_problem.teacher = request.user
            report_problem.save()
            messages.success(request, "レポート課題を更新しました")
            return redirect("grade:index")
    else:
        form = ReportProblemForm(instance=report_problem)
    return render(request, "grade/update_report_problem.html",
                  {"form": form, "report_problem": report_problem})


def delete_report_problem(request, report_problem_id):
    report_problem = get_object_or_404(ReportProblem, id=report_problem_id)
    if request.user != report_problem.teacher:
        return redirect("grade:index")
    report_problem.delete()
    messages.success(request, "レポート課題を削除しました")
    return redirect("grade:index")


def new_report(request, report_problem_id):
    report_problem = get_object_or_404(ReportProblem, id=report_problem_id)
    if request.method == "POST":
        if request.user.is_teacher:
            return redirect("grade:index")
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
    return render(request, "grade/new_report.html",
                  {"report_problem": report_problem, "form": form})
