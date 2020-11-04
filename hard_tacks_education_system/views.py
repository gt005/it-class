import datetime
import time
import locale

from braces import views
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, Http404
from django.views.generic import ListView, TemplateView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from .models import EducationTask, CheckedEducationTask, EducationLevel
from .addons_python.functions_for_tasks import save_task_solution, crete_level


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


class ActiveTask(LoginRequiredMixin, DetailView):
    template_name = "tacks_education_system/task_page.html"
    model = EducationTask
    login_url = "/login/"
    pk_url_kwarg = "pk"

    def post(self, request, **kwargs):
        return save_task_solution(request=request)  # returns JsonResponse

    def get_context_data(self, **kwargs):
        context = super(ActiveTask, self).get_context_data(**kwargs)
        context['task'] = kwargs.get('object')

        context['solved_tasks_list'] = CheckedEducationTask.objects.filter(
            original_task=self.request.user.puples.educationtask,
        ).order_by('-id')

        context['remainder_time_to_solve_a_task'] = int(
            (self.request.user.puples.educationtask.end_time - datetime.datetime.now()).total_seconds()
        ) - 1  # Секунда дана как время на загрузку страницы
        return context


class TasksList(LoginRequiredMixin, TemplateView):
    template_name = "tacks_education_system/tasks_list.html"
    login_url = "/login/"
    # TODO: Удалять все решения задач кроме самого последнего для экономии памяти

    def get_context_data(self, **kwargs):
        context = super(TasksList, self).get_context_data(**kwargs)
        context['level'] = self.request.user.puples.education_level
        context['active_task'] = self.request.user.puples.educationtask
        context['active_task_period'] = int((self.request.user.puples.educationtask.start_time - datetime.datetime.now()).total_seconds()) - 1  # Секунда дана как время на загрузку страницы

        point_of_start_count_remainder_time = datetime.datetime.now()
        if self.request.user.puples.educationtask.start_time > datetime.datetime.now():  # Задача еще не открылась
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
        message, http_status_code = crete_level(
            level_number=request.POST.get('level'),
            level_theme=request.POST.get('newTheme')
        )

        return JsonResponse({
            "message": message
        }, status=http_status_code)


class LevelSettings(views.LoginRequiredMixin,
                    views.SuperuserRequiredMixin,
                    DetailView):
    template_name = "tacks_education_system/system_settings/level_settings.html"
    login_url = "/login/"
    model = EducationLevel

    def patch(self, request, *args, **kwargs):
        print(request.kwargs)

    def get_object(self, *args, **kwargs):
        try:
            return self.model.objects.get(level_number=int(self.kwargs['level_number']))
        except (ValueError, ObjectDoesNotExist):
            raise Http404("Такая задача не найдена")


    def get_context_data(self, **kwargs):
        context = super(LevelSettings, self).get_context_data(**kwargs)
        context["level_object"] = self.object
        return context
