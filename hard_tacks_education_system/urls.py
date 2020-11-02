from django.urls import path

from . import views

urlpatterns = [
    path("", views.TasksList.as_view()),
    path("active_task/<int:pk>/", views.ActiveTask.as_view()),
    path("system_settings/", views.SystemSettings.as_view()),
    path("system_settings/level-settings/<int:level_number>", views.LevelSettings.as_view()),

]
