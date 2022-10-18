from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from . import views

urlpatterns = [
    path('', views.ExamPrepMain.as_view(), name='main_prep_exam'),
    path('<str:id_var>/', views.ExamPrepView.as_view(), name='task_page_prep_exam'),
    path('<str:id_var>/<int:task_num>', views.ExamPrepView.as_view(), name='task_page_prep_exam'),
    path('<str:id_var>/result', views.ExamPrepResult.as_view(), name='result_prep_exam')
    ]
