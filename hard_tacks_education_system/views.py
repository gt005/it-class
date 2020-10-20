from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, View
# from .models import EducationTask


class test(TemplateView):
    template_name = "tacks_education_system/task_page.html"
    # model = EducationTask
