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

        try:
            context['active_task'] = self.request.user.puples.educationtask
            point_of_start_count_remainder_time = datetime.datetime.now()
            context['active_task_period'] = int((self.request.user.puples.educationtask.start_time - datetime.datetime.now()).total_seconds()) - 1  # Секунда дана как время на загрузку страницы
            if self.request.user.puples.educationtask.start_time > datetime.datetime.now():  # Задача еще не открылась
                point_of_start_count_remainder_time = self.request.user.puples.educationtask.start_time
            context['active_task_period_remainder'] = int((self.request.user.puples.educationtask.end_time - point_of_start_count_remainder_time).total_seconds()) - 1  # Секунда дана как время на загрузку страницы
        except:  # Не смог найти RelatedObjectDoesNotExist
            context['active_task'] = None

        context['level'] = self.request.user.puples.education_level

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
            try:
                task_to_get_description = int(request.GET.get("get_task_description"))
                task_object_from_db = EducationTask.objects.get(
                    id=task_to_get_description
                )
            except TypeError:
                return JsonResponse({
                    "message": "Некорректный id задачи"
                }, status=415)
            except ObjectDoesNotExist:
                return JsonResponse({
                    "message": "Задача не найдена"
                }, status=404)

            description = {
                "task_id": task_object_from_db.id,
                "task_name": task_object_from_db.task_name,
                "start_time": datetime.datetime.strftime(task_object_from_db.start_time, "%d %B %Y г. %H:%M"),
                "end_time": datetime.datetime.strftime(task_object_from_db.end_time, "%d %B %Y г. %H:%M"),
                "description_task": task_object_from_db.description_task,
                "input_format": task_object_from_db.input_format,
                "output_format": task_object_from_db.output_format,
                "example_input_1": task_object_from_db.example_input_1,
                "example_output_1": task_object_from_db.example_output_1,
                "example_input_2": task_object_from_db.example_input_2,
                "example_output_2": task_object_from_db.example_output_2,
                "example_input_3": task_object_from_db.example_input_3,
                "example_output_3": task_object_from_db.example_output_3,
            }

            if task_object_from_db.for_student:
                description.update(
                    student_name=f"{task_object_from_db.for_student.name} {task_object_from_db.for_student.surname}"
                )
                description.update(
                    student_id=f"{task_object_from_db.for_student.id}"
                )

            if task_object_from_db.photo_1:
                description.update(photo_1=task_object_from_db.photo_1.url)
            if task_object_from_db.photo_1:
                description.update(photo_1=task_object_from_db.photo_1.url)
            if task_object_from_db.photo_1:
                description.update(photo_1=task_object_from_db.photo_1.url)

            return JsonResponse(description, status=200)
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
        elif request.POST.get("deleteTask"):
            return delete_task_from_db(  # returns JsonResponse
                task_id=request.POST.get("taskToDeleteId"),
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
        context["task_amount"] = len(context["tasks_with_this_level"])
        context["students_amount"] = get_amount_of_people_with_level(self.object.level_number)
        return context


class EditLevel(views.LoginRequiredMixin,
                views.SuperuserRequiredMixin,
                DetailView):
    template_name = "tacks_education_system/system_settings/task_edit.html"
    model = EducationTask
    login_url = "/login/"
    pk_url_kwarg = "edit_task_id"

    def get_context_data(self, **kwargs):
        context = super(EditLevel, self).get_context_data(**kwargs)

        context['task'] = kwargs.get('object')

        return context
