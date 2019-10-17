from django.contrib import admin
from grade.models import Grade
from grade.models import Report
from grade.models import ReportProblem


class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'english', 'math', 'japanese', 'gpa')
    list_display_links = ('id', 'user')


class ReportProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'teacher')
    list_display_links = ('id', 'title')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'report_problem')
    list_display_links = ('id', 'student')


admin.site.register(Grade, GradeAdmin)
admin.site.register(ReportProblem, ReportProblemAdmin)
admin.site.register(Report, ReportAdmin)
