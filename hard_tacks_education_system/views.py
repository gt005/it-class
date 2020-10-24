import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.generic import ListView, TemplateView, View
# from .models import EducationTask


class ActiveTask(TemplateView):
    template_name = "tacks_education_system/task_page.html"

    def post(self, request):
        if request.POST.get('taskSolutionType') == 'code':
            return JsonResponse({
                'message': ' Прислан код на языке ' + request.POST.get('codeLang')
            })
        elif request.POST.get('taskSolutionType') == 'file':
            print(request.FILES.get('taskSolutionFile').open().read())
            return JsonResponse({
                'message': ' Прислан файл с именем ' + str(request.FILES.get('taskSolutionFile'))
            })
        return HttpResponseBadRequest()

    def get_context_data(self, **kwargs):
        context = super(ActiveTask, self).get_context_data(**kwargs)
        context['remainder_time_to_solve_a_task'] = (datetime.datetime(2020, 10, 21, 22, 48, 30) - datetime.datetime.now()).seconds - 1  # Секунда дана как время на загрузку страницы
        return context

