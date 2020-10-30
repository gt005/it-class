import datetime
import time
import locale

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.generic import ListView, TemplateView, View


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


class ActiveTask(TemplateView):
    template_name = "tacks_education_system/task_page.html"

    def post(self, request):
        if request.POST.get('taskSolutionType') == 'code':
            return JsonResponse({
                'message': ' Прислан код на языке ' + request.POST.get('codeLang'),
                'solutionTime': time.strftime('%d %b %Y, %H:%M:%S'),
            })
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
        context['remainder_time_to_solve_a_task'] = (datetime.datetime(2020, 10, 21, 22, 48, 30) - datetime.datetime.now()).seconds - 1  # Секунда дана как время на загрузку страницы
        return context


class TasksList(TemplateView):
    template_name = "tacks_education_system/tasks_list.html"

    def get_context_data(self, **kwargs):
        context = super(TasksList, self).get_context_data(**kwargs)
        context['level'] = 5
        context['active_task_period'] = 10
        return context
