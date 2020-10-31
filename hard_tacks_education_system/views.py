import datetime
import time
import locale

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.generic import ListView, TemplateView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from .models import EducationTask, CheckedEducationTask


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


class ActiveTask(LoginRequiredMixin, DetailView):
    template_name = "tacks_education_system/task_page.html"
    model = EducationTask
    login_url = "/login/"
    pk_url_kwarg = "pk"

    def post(self, request, **kwargs):
        if request.POST.get('taskSolutionType') == 'code':
            return JsonResponse({
                'message': ' Прислан код на языке ' + request.POST.get('codeLang'),
                'solutionTime': time.strftime('%d %b %Y, %H:%M:%S'),
            }, status=400)
        elif request.POST.get('taskSolutionType') == 'file':
            file_code = request.FILES.get('taskSolutionFile').open().read()
            return JsonResponse({
                'message': ' Прислан файл с именем ' + str(request.FILES.get('taskSolutionFile')),
                'solutionTime': time.strftime('%d %b %Y, %H:%M:%S'),
                'solutionCode': file_code.decode('utf-8'),
            })
        return HttpResponseBadRequest()

    def get_context_data(self, **kwargs):
        context = super(ActiveTask, self).get_context_data(**kwargs)
        context['task'] = kwargs.get('object')
        context['remainder_time_to_solve_a_task'] = (datetime.datetime(2020, 10, 21, 22, 48, 30) - datetime.datetime.now()).seconds - 1  # Секунда дана как время на загрузку страницы
        return context


class TasksList(LoginRequiredMixin, TemplateView):
    template_name = "tacks_education_system/tasks_list.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super(TasksList, self).get_context_data(**kwargs)
        context['level'] = self.request.user.puples.education_level
        context['active_task_period'] = 150 * 60
        return context
