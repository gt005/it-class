from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from . import views

urlpatterns = [
    path('', views.DayTaskView.as_view(), name='Задача дня'),
    ]
