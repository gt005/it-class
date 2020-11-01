from django.urls import path

from . import views

urlpatterns = [
    path("", views.TasksList.as_view()),
    path("active_task/<int:pk>/", views.ActiveTask.as_view()),

    path("system_settings/levels/", views.TaskSettingsLevels.as_view()),
]
