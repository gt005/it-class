from django.urls import path

from . import views

urlpatterns = [
    path("", views.test.as_view()),

]
