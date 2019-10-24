from django.contrib import admin
from .models import Grade, Report, ReportProblem, Profile, CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'english', 'math', 'japanese', 'gpa')
    list_display_links = ('id', 'user')


class ReportProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'teacher')
    list_display_links = ('id', 'title')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'report_problem', 'created_datetime')
    list_display_links = ('id', 'student')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher')
    list_display_links = ('id', 'teacher')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'is_teacher']

    # fields of edit CustomUser form
    fieldsets = (
        (None, {'fields': ('username', 'is_teacher')}),
    )

    # fields of create CustomUser form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_teacher'),
        }),
    )


admin.site.register(Grade, GradeAdmin)
admin.site.register(ReportProblem, ReportProblemAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
