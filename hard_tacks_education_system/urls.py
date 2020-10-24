from django.urls import path

from . import views

urlpatterns = [
    path("active_task/", views.ActiveTask.as_view()),

]
