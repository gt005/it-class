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
from .addons_python.functions_for_tasks import *


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
    # TODO: Удалять все решения после закрытие задачи кроме самого последнего для экономии памяти

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

    def get(self, request, *args, **kwargs):
        if request.GET:
            return JsonResponse({
                "task_name": "Путешествие к звездам " + request.GET.get("get_task_description"),
                "start_time": "11/17/2020 1:12 AM",
                "end_time": "11/17/2020 1:12 AM",
                "description_task": '''Узник пытается бежать из замка, который состоит из MN квадратных комнат, расположенных в виде прямоугольника M×N. Между любыми двумя соседними комнатами есть дверь , однако некоторые комнаты закрыты и попасть в них нельзя. В начале узник находится в угловой комнате и для спасения ему надо попасть в противоположную угловую комнату. Времени у него немного, всего он может побывать не более, чем в M+N-1 комнате, включая начальную и конечную комнату на своем пути, то есть с каждым переходом в соседнюю комнату расстояние до выхода из замка должно уменьшаться. От вас требуется найти количество различных маршрутов, ведущих к спасению.''',
                "input_format": "Первая строчка входных данных содержит натуральные числа M и N, не превосходящих 1000. Далее идет план замка в виде M строчек из N символов в каждой. Один символ соответствует одной комнате: если символ равен 1, то в комнату можно попасть, если он равен 0, то комната закрыта. Первоначальное положение узника – левый нижний угол (первый символ последней строки), выход находится в правом верхнем углу (последний символ первой строки, оба этих символа равны 1).",
                "output_format": '''Программа должна напечатать количество маршрутов, ведущих узника к выходу и проходящих через M+N-1 комнату, или слово impossible, если таких маршрутов не существует. 

Входные данные подобраны таким образом, что искомое число маршрутов не превосходит 2.000.000.000.''',

            }, status=200)
        else:
            return super(LevelSettings, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            level_to_change_number = int(kwargs.get("level_number"))
            level_object_from_db = EducationLevel.objects.get(
                level_number=level_to_change_number
            )
        except TypeError:
            return JsonResponse({
                "message": "Неправильный номер уровня"
            }, status=415)
        except ObjectDoesNotExist:
            return JsonResponse({
                "message": "Уровень с таким номером не найден"
            }, status=404)

        if request.POST.get("newTheme"):
            return change_level_theme(  # returns JsonResponse
                new_theme=request.POST.get("newTheme"),
                for_level=level_object_from_db,
            )
        elif request.POST.get("createNewTask"):
            return create_task_and_add_to_db(  # returns JsonResponse
                post_request_object=request.POST,
                level_object_from_db=level_object_from_db
            )

    def get_object(self, *args, **kwargs):
        try:
            return self.model.objects.get(
                level_number=int(self.kwargs["level_number"])
            )
        except (ValueError, ObjectDoesNotExist):
            raise Http404("Такая задача не найдена")

    def get_context_data(self, **kwargs):
        context = super(LevelSettings, self).get_context_data(**kwargs)
        context["level_object"] = self.object
        context["tasks_with_this_level"] = EducationTask.objects.filter(
            task_level=self.object
        )
        return context
