import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, View
# from .models import EducationTask


class test(TemplateView):
    template_name = "tacks_education_system/task_page.html"

    def get_context_data(self, **kwargs):
        context = super(test, self).get_context_data(**kwargs)
        context['remined_time_to_solve_a_task'] = (datetime.datetime(2020, 10, 21, 22, 48, 30) - datetime.datetime.now()).seconds - 1  # Секунда дана как время на загрузку страницы
        return context

