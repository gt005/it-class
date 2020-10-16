from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from . import views

urlpatterns = [
    path('', views.DayTaskView.as_view(), name='Задача дня'),
    path('delete_task/<int:id>', views.DayTaskView.as_view(), name='Задача дня'),
    path('add/', views.DayTaskAddView.as_view(), name='Добавить задачу дня'),
    path('show/<int:id>', views.DayTaskShowView.as_view(), name='Отображении задачи дня'),
    path('edit/<int:id>', views.DayTaskEditView.as_view(), name='Редактирование задачи дня'),
    ]
