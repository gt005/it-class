from django.urls import path

from . import views

urlpatterns = [
    path("active_task/", views.test.as_view()),

]
