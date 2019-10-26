from django.urls import path
from . import views, views_grade, views_report
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import BoardViewSet

app_name = 'grade'
urlpatterns = [
    path('', views.index, name='index'),

    path('signup/', views.signup, name='signup'),
    path('login/',
         auth_views.LoginView.as_view(template_name='grade/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('new_grade/<int:user_id>/', views_grade.new_grade, name='new_grade'),
    path('update_grade/<int:user_id>/', views_grade.update_grade,
         name='update_grade'),
    path('show_grade/', views_grade.show_grade, name='show_grade'),

    path('new_report_problem/', views_report.new_report_problem,
         name='new_report_problem'),
    path('update_report_problem/<int:report_problem_id>/',
         views_report.update_report_problem,
         name='update_report_problem'),
    path('delete_report_problem/<int:report_problem_id>/',
         views_report.delete_report_problem,
         name='delete_report_problem'),

    path('new_report/<int:report_problem_id>/',
         views_report.new_report, name='new_report'),

    path('new_board/', views.new_board, name='new_board'),
    path('delete_board/<int:board_id>', views.delete_board, name='delete_board'),

    path('new_profile/', views.new_profile, name='new_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

router = routers.DefaultRouter()
router.register(r'boards', BoardViewSet)