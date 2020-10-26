from django.urls import path

from . import views

urlpatterns = [
    path("", views.TasksList.as_view()),
    path("active_task/", views.ActiveTask.as_view()),

]
