# TODO: Сделать просмотр статистики учеников
#  Сделать общий граф успеваемости

# Пароли от system_tester_(number) - UYbiwe982

import datetime
import time
import locale

from braces import views
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, Http404, HttpResponseForbidden
from django.views.generic import ListView, TemplateView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from mainapp.models import Puples

from .models import EducationTask, CheckedEducationTask, EducationLevel
from .addons_python.functions_for_tasks import *
from itclass.settings import AVAILABLE_LANGUAGES_LIST


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


class ActiveTask(LoginRequiredMixin, DetailView):
    template_name = "tacks_education_system/task_page.html"
    model = EducationTask
    login_url = "/login/"
    pk_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        if self.get_object().for_student != request.user.puples and \
                get_object_from_db(CheckedEducationTask, {
                    "solved_user": request.user.puples,
                    "original_task": self.get_object()
                }) is None:
            return HttpResponseForbidden()
        return super(ActiveTask, self).get(request, *args, **kwargs)

    def post(self, request, **kwargs):
        if self.get_object().for_student != request.user.puples and \
                get_object_from_db(CheckedEducationTask, {
                    "solved_user": request.user.puples,
                    "original_task": self.get_object()
                }) is None:
            return HttpResponseForbidden()
        return save_task_last_solution(request=request)  # returns JsonResponse

    def get_context_data(self, **kwargs):
        context = super(ActiveTask, self).get_context_data(**kwargs)
        context["tasks_amount_to_check"] = len(list(filter(
            lambda task: task.result_summ_mark is None,
            CheckedEducationTask.objects.filter(
                Q(first_peer=self.request.user.puples) |
                Q(second_peer=self.request.user.puples)
            )
        )))

        context['task'] = kwargs.get('object')

        context['solved_tasks_list'] = CheckedEducationTask.objects.filter(
            original_task=context['task'],
            solved_user=self.request.user.puples
        ).order_by('-id')

        context['remainder_time_to_solve_a_task'] = int(
            (context['task'].end_time - datetime.datetime.now()).total_seconds()) - 1
        # Секунда дана как время на загрузку страницы
        return context


class TasksList(LoginRequiredMixin, TemplateView):
    template_name = "tacks_education_system/tasks_list.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super(TasksList, self).get_context_data(**kwargs)

        context["tasks_amount_to_check"] = len(list(filter(
            lambda task: task.result_summ_mark is None,
            CheckedEducationTask.objects.filter(
                Q(first_peer=self.request.user.puples) |
                Q(second_peer=self.request.user.puples)
            )
        )))

        context['level'] = self.request.user.puples.education_level
        context['previous_tasks'] = CheckedEducationTask.objects.filter(
            solved_user=self.request.user.puples
        ).order_by("-solution_time")

        if not check_existing_active_task(self.request.user.puples):
            return context

        try:
            context['active_task'] = self.request.user.puples.educationtask
            point_of_start_count_remainder_time = datetime.datetime.now()
            context['active_task_period'] = int((self.request.user.puples.educationtask.start_time - datetime.datetime.now()).total_seconds()) - 1  # Секунда дана как время на загрузку страницы
            if self.request.user.puples.educationtask.start_time > datetime.datetime.now():  # Задача еще не открылась
                point_of_start_count_remainder_time = self.request.user.puples.educationtask.start_time
            context['active_task_period_remainder'] = int((self.request.user.puples.educationtask.end_time - point_of_start_count_remainder_time).total_seconds()) - 1  # Секунда дана как время на загрузку страницы
        except:  # Не смог найти RelatedObjectDoesNotExist
            context['active_task'] = None

        return context


class SystemSettings(views.LoginRequiredMixin,
                     views.SuperuserRequiredMixin,
                     ListView):
    template_name = "tacks_education_system/system_settings/settings_main.html"
    login_url = "/login/"
    model = EducationLevel
    ordering = "level_number"

    def get(self, request, *args, **kwargs):
        if request.GET:
            try:
                level_to_get_description = int(
                    request.GET.get("get_level_description")
                )
                level_object_from_db = EducationLevel.objects.get(
                    level_number=level_to_get_description
                )
            except TypeError:
                return JsonResponse({
                    "message": "Некорректный id задачи"
                }, status=415)
            except ObjectDoesNotExist:
                return JsonResponse({
                    "message": "Задача не найдена"
                }, status=404)

            return JsonResponse({
                "fullness_percents": get_level_fullness_percents(
                    level_to_get_description
                ),
                "success_average_score": get_level_average_score(
                    level_object_from_db
                )
            }, status=200)

        return super(SystemSettings, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        message, http_status_code = crete_level(
            level_number=request.POST.get('level'),
            level_theme=request.POST.get('newTheme')
        )

        return JsonResponse({
            "message": message
        }, status=http_status_code)

    def get_context_data(self, *args, **kwargs):
        context = super(SystemSettings, self).get_context_data(*args, **kwargs)

        context["tasks_amount_to_check"] = len(list(filter(
            lambda task: task.result_summ_mark is None,
            CheckedEducationTask.objects.filter(
                Q(first_peer=self.request.user.puples) |
                Q(second_peer=self.request.user.puples)
            )
        )))

        return context


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
            if task_object_from_db.photo_2:
                description.update(photo_2=task_object_from_db.photo_2.url)
            if task_object_from_db.photo_3:
                description.update(photo_3=task_object_from_db.photo_3.url)

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
                request_object=request,
                level_object_from_db=level_object_from_db
            )
        elif request.POST.get("deleteTask"):
            return delete_task_from_db(  # returns JsonResponse
                task_id=request.POST.get("taskToDeleteId"),
            )
        elif request.POST.get("setTasksToStudents"):
            return distribute_tasks_among_students(  # returns JsonResponse
                level_number=self.get_object().level_number
            )
        elif request.POST.get("setTimeToAllTasks"):
            return set_time_to_all_level_tasks(
                level=level_object_from_db,
                start_time=request.POST.get("startTime"),
                end_time=request.POST.get("endTime")
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
        context["tasks_amount_to_check"] = len(list(filter(
            lambda task: task.result_summ_mark is None,
            CheckedEducationTask.objects.filter(
                Q(first_peer=self.request.user.puples) |
                Q(second_peer=self.request.user.puples)
            )
        )))

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

    def post(self, request, *args, **kwargs):
        try:
            task_to_get_description = int(kwargs["edit_task_id"])
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

        return change_task_data_in_model(
            request_object=request,
            for_task=task_object_from_db
        )

    def get_context_data(self, **kwargs):
        context = super(EditLevel, self).get_context_data(**kwargs)

        context["tasks_amount_to_check"] = len(list(filter(
            lambda task: task.result_summ_mark is None,
            CheckedEducationTask.objects.filter(
                Q(first_peer=self.request.user.puples) |
                Q(second_peer=self.request.user.puples)
            )
        )))

        context['task'] = kwargs.get('object')
        return context


class StudentsStatistic(views.LoginRequiredMixin,
                        views.SuperuserRequiredMixin,
                        ListView):
    template_name = "tacks_education_system/system_settings/students_statistic.html"
    model = Puples
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        if request.POST.get("get_data_from_user_id"):
            return get_student_statistic(
                request_object=request
            )  # returns JsonResponse

    def get_context_data(self, *args, **kwargs):
        context = super(StudentsStatistic, self).get_context_data(*args, **kwargs)
        context["tasks_amount_to_check"] = len(list(filter(
            lambda task: task.result_summ_mark is None,
            CheckedEducationTask.objects.filter(
                Q(first_peer=self.request.user.puples) |
                Q(second_peer=self.request.user.puples)
            )
        )))

        context["students_list"] = self.model.objects.filter(
            Q(status="ST10") | Q(status="ST11")
        ).order_by('surname', 'name')
        context["status_choices"] = sorted(list(
            {people.get_status_display() for people in context["students_list"]}
        ))
        return context


class TasksEstimate(views.LoginRequiredMixin,
                    ListView):
    template_name = "tacks_education_system/estimate_tasks.html"
    model = CheckedEducationTask
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        distribute_tasks_for_estimate()
        return super(TasksEstimate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        set_estimate_rate(request_object=request)

        return redirect("/tasks/estimate_tasks/")

    def get_context_data(self, *args, **kwargs):
        context = super(TasksEstimate, self).get_context_data(*args, **kwargs)

        context["estimated_tasks"] = self.model.objects.filter(
            Q(first_peer=self.request.user.puples) |
            Q(second_peer=self.request.user.puples)
        )

        context["tasks_amount_to_check"] = len(list(filter(
            lambda task: task.result_summ_mark is None,
            CheckedEducationTask.objects.filter(
                Q(first_peer=self.request.user.puples) |
                Q(second_peer=self.request.user.puples)
            )
        )))

        context['lang_list'] = AVAILABLE_LANGUAGES_LIST
        return context


class SetStartStudentSettings(views.LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.GET.get("getLanguagesList"):
            return JsonResponse({"languages": AVAILABLE_LANGUAGES_LIST}, status=200)

    def post(self, request, *args, **kwargs):
        if request.POST.get('actionSetProgrammingLanguages') == 'true':
            languages_list = []

            for language in request.POST:
                if str(language).startswith('setProgrammingLanguage'):
                    if request.POST.get(language) in AVAILABLE_LANGUAGES_LIST:
                        languages_list.append(request.POST.get(language))
                    else:
                        return JsonResponse(
                            {"message": 'wrong language'},
                            status=400
                        )
            if not languages_list:
                return JsonResponse(
                    {"message": 'Empty lang set'},
                    status=400
                )

            request.user.puples.task_education_addition_data['known_languages'] = languages_list
            request.user.puples.save()

            return JsonResponse({"message": 'languages added'}, status=200)
