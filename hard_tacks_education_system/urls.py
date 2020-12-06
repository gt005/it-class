from django.urls import path

from . import views

urlpatterns = [
    path("", views.TasksList.as_view()),
    path("active_task/<int:pk>/", views.ActiveTask.as_view()),
    path("system_settings/", views.SystemSettings.as_view()),
    path("estimate_tasks/", views.TasksEstimate.as_view()),
    path("students_statistic/", views.StudentsStatistic.as_view()),
    path("system_settings/level-settings/<level_number>", views.LevelSettings.as_view()),
    path("system_settings/level-settings/edit-task/<edit_task_id>", views.EditLevel.as_view())

]
