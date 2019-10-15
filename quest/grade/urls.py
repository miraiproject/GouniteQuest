from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'grade'
urlpatterns = [
    path('', views.index, name='index'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='grade/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('new_grade/<int:user_id>/', views.new_grade, name='new_grade'),
    path('new_report_problem/', views.new_report_problem, name='new_report_problem'),
    path('new_report/<int:report_problem_id>/', views.new_report, name='new_report'),
    path('new_board/', views.new_board, name='new_board'),

]
