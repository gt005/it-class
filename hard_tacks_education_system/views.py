import datetime
import time
import locale

from braces import views
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, \
    HttpResponseNotFound
from django.views.generic import ListView, TemplateView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from .models import EducationTask, CheckedEducationTask, EducationLevel
from .addons_python.functions_for_tasks import save_task_solution


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


class ActiveTask(LoginRequiredMixin, DetailView):
    template_name = "tacks_education_system/task_page.html"
    model = EducationTask
    login_url = "/login/"
    pk_url_kwarg = "pk"

    def post(self, request, **kwargs):
        if request.POST.get("taskSolutionType") == "code":
            result_message, http_code, task_id = save_task_solution(
                programm_code=request.POST.get("codeText"),
                programm_code_language=request.POST.get("codeLang"),
                request=request
            )

            if task_id is not None:
                solution_task_from_db = CheckedEducationTask.objects.get(id=task_id)

            return JsonResponse({
                "message": result_message,
                "solutionTime": solution_task_from_db.get_solution_time(),
                "solutionId": task_id
            }, status=http_code)
        elif request.POST.get("taskSolutionType") == "file":
            try:
                file_code = request.FILES.get("taskSolutionFile").open().read().decode("utf-8")
            except TypeError:
                return JsonResponse({
                    "message": "Пустой файл",
                }, status=400)

            result_message, http_code, task_id = save_task_solution(
                programm_code=file_code,
                programm_code_language=request.POST.get("codeLang"),
                request=request
            )
            solution_task_from_db = CheckedEducationTask.objects.get(id=task_id)

            return JsonResponse({
                "message": result_message,
                "solutionTime": solution_task_from_db.get_solution_time(),
                "solutionCode": file_code,
                "solutionId": task_id
            }, status=http_code)
        return HttpResponseBadRequest()

    def get_context_data(self, **kwargs):
        context = super(ActiveTask, self).get_context_data(**kwargs)
        context['task'] = kwargs.get('object')
        context['solved_tasks_list'] = CheckedEducationTask.objects.filter(
            original_task=self.request.user.puples.educationtask,
        ).order_by('-id')
        context['remainder_time_to_solve_a_task'] = int((self.request.user.puples.educationtask.end_time - datetime.datetime.now(datetime.timezone.utc)).total_seconds()) - 1  # Секунда дана как время на загрузку страницы
        return context


class TasksList(LoginRequiredMixin, TemplateView):
    template_name = "tacks_education_system/tasks_list.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super(TasksList, self).get_context_data(**kwargs)
        context['level'] = self.request.user.puples.education_level
        context['active_task'] = self.request.user.puples.educationtask
        context['active_task_period'] = int((self.request.user.puples.educationtask.start_time - datetime.datetime.now(datetime.timezone.utc)).total_seconds()) - 1  # Секунда дана как время на загрузку страницы

        point_of_start_count_remainder_time = datetime.datetime.now(datetime.timezone.utc)
        if self.request.user.puples.educationtask.start_time > datetime.datetime.now(datetime.timezone.utc):
            point_of_start_count_remainder_time = self.request.user.puples.educationtask.start_time
        context['active_task_period_remainder'] = int((self.request.user.puples.educationtask.end_time - point_of_start_count_remainder_time).total_seconds()) - 1  # Секунда дана как время на загрузку страницы

        return context


class SystemSettings(views.LoginRequiredMixin,
                         views.SuperuserRequiredMixin,
                         ListView):
    template_name = "tacks_education_system/system_settings/settings_main.html"
    login_url = "/login/"
    model = EducationLevel
    ordering = "level_number"

    def post(self, request, **kwargs):
        ''' TODO: Перенести эту функцию в functions_for_tasks.py '''
        for_level = request.POST.get('level')
        level_theme = request.POST.get('newTheme')
        last_exist_level = self.model.objects.all()
        if last_exist_level:
            last_exist_level = last_exist_level.order_by('-level_number')[0]
        else:
            last_exist_level = 0

        try:
            for_level = int(for_level)
        except ValueError:
            print('Incorrect level')
            return JsonResponse({
                'message': 'Incorrect level.'
            }, status=400)

        if last_exist_level.level_number + 1 != for_level:
            print('Not needed level')
            return JsonResponse({
                'message': 'Not needed level.'
            }, status=400)

        if len(str(level_theme)) > 255:
            print('Length of level theme is more then 255 chars')
            return JsonResponse({
                'message': 'Length of level theme is more then 255 chars.'
            }, status=400)

        self.model(level_number=for_level, level_theme=level_theme).save()

        return JsonResponse({
            'message': 'Уровень успешно создан.'
        })


class LevelSettings(views.LoginRequiredMixin,
                    views.SuperuserRequiredMixin,
                    ListView):
    template_name = "tacks_education_system/system_settings/level_settings.html"
    login_url = "/login/"
    model = EducationLevel
    ordering = "level_number"