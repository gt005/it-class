from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, View
# from .models import EducationTask


class test(TemplateView):
    template_name = "hard_tacks_education_system/hard_tacks_education_system_base_template.html"
    # model = EducationTask
