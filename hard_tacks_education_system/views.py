import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.generic import ListView, TemplateView, View
# from .models import EducationTask


class ActiveTask(TemplateView):
    template_name = "tacks_education_system/task_page.html"

    def post(self, request):
        try:
            data = json.loads(request.body.decode())
        except ValueError:
            return JsonResponse({
                'error': 'пусто',
            })

        if data.get('taskSolutionType') == 'code':
            return JsonResponse({
                'message': data.get('codeText') + '    ' + data.get('codeLang')
            })
        elif data.get('taskSolutionType') == 'file':
            print(data.get('taskAnswerFile'))
            return JsonResponse({
                'message': data.get('taskAnswerFile')
            })
        return HttpResponseBadRequest()


    def get_context_data(self, **kwargs):
        context = super(ActiveTask, self).get_context_data(**kwargs)
        context['remined_time_to_solve_a_task'] = (datetime.datetime(2020, 10, 21, 22, 48, 30) - datetime.datetime.now()).seconds - 1  # Секунда дана как время на загрузку страницы
        return context

