import datetime
import datetime as dt
import os
import re

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from docxtpl import DocxTemplate
from .addons_python.stepic_ege import get_stepic_info, get_csv_file_stepic, get_info_for_all_class
from .addons_python.checker_class_11 import checker
from .addons_python.list_v2 import checker_list_v1

from .addons_python.views_addons_classes import HeaderNotificationsCounter
from .addons_python.notifications import send_mail_to_applicant, send_telegram
from .addons_python.views_addons_functions import recount_all_peoples_rating
from .forms import EventsForm, AddEventForm, ImgChangeForm, CollectData
from .models import Puples, Events, Works, DaysTask, ApplicantAction, SummerPractice, EventActive
from django.views.generic.base import TemplateView, View
from django.shortcuts import render

def test(request):
    return render(request, 'test/index.html', {})

class MainView(HeaderNotificationsCounter, ListView):
    puple = Puples
    queryset = Puples.objects.all()
    template_name = "main_page/main_page.html"


class HacatonView(HeaderNotificationsCounter, ListView):
    model = Puples
    template_name = "hacaton.html"


class WrongTasksView(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    model = DaysTask
    template_name = "task_day_wrong.html"
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['score'] = len([int(i) for i in DaysTask.objects.get().id_answers.split()])
        return context


class TasksView(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    model = DaysTask
    template_name = "task_day.html"
    mass_rate = [5, 3]
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.puples.status == "APP":
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_list_solved_task(self, x):
        return [(Puples.objects.get(user_id=i).surname, Puples.objects.get(user_id=i).name) for i in x]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_task'] = DaysTask.objects.get().name_task
        context['discription_task'] = DaysTask.objects.get().discription_task
        context['date_task'] = DaysTask.objects.get().date
        context['count_of_answer'] = DaysTask.objects.get().count_answer
        context['count_of_puples'] = -DaysTask.objects.get().count_answer
        context['list_answ'] = [int(i) for i in DaysTask.objects.get().id_answers.split()]
        context['score'] = len([int(i) for i in DaysTask.objects.get().id_answers.split()])
        context['list_wins'] = self.get_list_solved_task(context['list_answ'])
        return context

    def post(self, request):
        if request.POST["result"] == DaysTask.objects.get().result and DaysTask.objects.get().count_answer < 0:
            Events.objects.create(name=f"Задача дня \"{DaysTask.objects.get().name_task}\"", date=datetime.date.today(),
                                  organization="ГБОУ Школа 1158",
                                  events=Puples.objects.get(user=request.user.id),
                                  event_rate=self.mass_rate[DaysTask.objects.get().count_answer], check=True,
                                  verification_file="123.jpg")
            task = DaysTask.objects.get()
            task.count_answer += 1
            task.id_answers += str(Puples.objects.get(user=request.user.id).user.id) + " "
            task.save()
            return redirect("/task_day")
        return redirect("/task_day/wrong")


def verificationFileDownload(request):
    usr_pk = request.POST.get("usr_pk")
    if not (request.user.is_superuser or str(request.user.pk) == usr_pk):
        return HttpResponseForbidden()
    file_base_dir = request.POST.get("file_base_dir")
    file_path = os.path.join(settings.MEDIA_ROOT, file_base_dir)
    try:
        with open(file_path, "rb") as file:
            response = HttpResponse(file.read(), content_type="application")
            response['Content-Disposition'] = 'inline; filename="verification' + os.path.splitext(file_base_dir)[
                1] + '"'
            return response
    except FileNotFoundError:
        return HttpResponseNotFound()


class PuplesView(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    puple = Puples
    template_name = "puples/puples_list.html"
    queryset = Puples.objects.order_by("-rate")
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.puples.status == "APP":
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        recount_all_peoples_rating()

        context = super().get_context_data(**kwargs)
        context['superusr'] = self.request.user.is_superuser
        context['pupil_pk'] = self.request.user.puples.pk
        return context


class ApplicantListView(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    puple = Puples
    template_name = "applicant_list.html"
    queryset = Puples.objects.filter(status="APP").order_by('-applicant_first_result')
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.puples.status == "APP":
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        recount_all_peoples_rating()

        context = super().get_context_data(**kwargs)
        context['superusr'] = self.request.user.is_superuser
        context['pupil_pk'] = self.request.user.puples.pk
        context['app_without_interview'] = Puples.objects.filter(status="APP").count() - Puples.objects.filter(
            status="APP", applicant_progress="75").count()
        return context


def account(request):
    var = request.user.puples.pk
    return redirect("/statistic/pupil/" + str(var))


class ImgChangeView(HeaderNotificationsCounter, LoginRequiredMixin, DetailView):
    model = Puples
    pk_url_kwarg = "pk"
    template_name = "img_change.html"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events_count'] = Events.objects.filter(events__pk=self.kwargs['pk'], check=True).count()
        context['allevents'] = Events.objects.filter(events__pk=self.kwargs['pk']).order_by('-date')
        if Puples.objects.get(pk=self.kwargs["pk"]).status == "APP":
            context['app'] = ApplicantAction.objects.get(action_app=self.kwargs['pk'])
        else:
            context['app'] = 1
        return context

    def get(self, request, pk):
        if request.user.is_superuser or request.user.puples.pk == pk:
            return super().get(request, pk)
        return HttpResponseForbidden()

    def post(self, request, pk):
        puple = request.user.puples
        form = ImgChangeForm(request.POST, request.FILES, instance=puple)
        if form.is_valid():
            form.save()
            return redirect("/statistic/pupil/" + str(pk))
        return redirect(reverse_lazy("img_change", kwargs={'pk': pk}))


class PostDetailView(HeaderNotificationsCounter, LoginRequiredMixin, DetailView):
    model = Puples
    pk_url_kwarg = "pk"
    template_name = "puple_detail/puples_detail_end.html"
    login_url = '/login/'

    def post(self, request, pk):
        form = CollectData(request.POST)
        if "update_file_csv" in request.POST and request.POST['update_file_csv']:
            link_stepic = request.POST['update_file_csv']
            get_csv_file_stepic(link_stepic)
            return redirect("/statistic/pupil/" + str(pk))
        else:
            if form.is_valid():
                print('ok')
                a = Puples.objects.get(user=request.user.id)
                form = CollectData(request.POST, instance=a)
                form.save()

                return redirect("/statistic/pupil/" + str(pk))
            else:
                a = ApplicantAction.objects.get(action_app=pk)
                a.check = True
                a.save()
                return redirect("/statistic/pupil/" + str(pk))
        return redirect("/statistic/pupil/" + str(pk))

    def get(self, request, pk):
        if request.user.is_superuser or request.user.puples.pk == pk:

            if "edit_data" in request.GET:
                if request.user.puples.pk != pk and not request.user.is_superuser:
                    # Если пытается изменить не свой email и не является админом
                    return HttpResponseForbidden()

                if (request.COOKIES.get("csrftoken") != request.GET.get("token")):
                    return HttpResponseForbidden()

                student = Puples.objects.get(id=pk)

                message = "Неверный формат запроса"
                if request.GET.get("edit_data") == 'tel':
                    mobile_number_regular = re.compile(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{9,10}$')
                    new_number = request.GET.get("tel")
                    if mobile_number_regular.match(new_number):
                        # TODO: Сделать форматирование номера под стандарт 81231231212
                        student.phone = new_number
                        student.save()
                        message = "success"
                    else:
                        message = "Неправильный формат номера"

                elif request.GET.get("edit_data") == 'email':
                    email_regular = re.compile(r'(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
                    new_email = request.GET.get("email")
                    if email_regular.match(new_email):
                        student.email = new_email
                        student.save()
                        message = "success"  # "Почта успешно изменена!"
                    else:
                        message = "Неправильный формат почты"
                return JsonResponse({"message": message})

            return super().get(request, pk)
        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['active_task'] = list(filter(lambda x: x.date >= datetime.datetime.now().date(), EventActive.objects.all().order_by('date')))[:5]
        print(context['active_task'])
        context['events_count'] = Events.objects.filter(events__pk=self.kwargs['pk'], check=True).count()
        context['allevents'] = filter(lambda x: not x.name.startswith("Задача дня"), Events.objects.filter(events__pk=self.kwargs['pk']).order_by('-date'))
        context['alldaytasks'] = filter(lambda x: x.name.startswith("Задача дня"),
                                      Events.objects.filter(events__pk=self.kwargs['pk']).order_by('-date'))
        context['form'] = CollectData()
        if Puples.objects.get(pk=self.kwargs["pk"]).status == "APP":
            context['app'] = ApplicantAction.objects.get(action_app=self.kwargs['pk'])
        else:
            context['app'] = 1
        context['rate_event'] = sum(
            map(lambda x: x.event_rate, Events.objects.filter(events__pk=self.kwargs['pk'], check=True)))
        puple_info_stepic = get_stepic_info(Puples.objects.get(id=context['pk']).user.id)
        context["info_all_class"] = get_info_for_all_class()
        try:
            context["data_stepic"] = puple_info_stepic[-27:]
            context["procent_success"] = puple_info_stepic[-29]
            context["tasks_success"] = puple_info_stepic[-30]
            context["unsolved_tasks"] = puple_info_stepic[-28] - puple_info_stepic[-30]
        except:
            print("empty_list")
        return context


class AddEventView(HeaderNotificationsCounter, LoginRequiredMixin, DetailView):
    model = Puples
    pk_url_kwarg = "pk"
    template_name = "add_event/add_event.html"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events_count'] = Events.objects.filter(events__pk=self.kwargs['pk'], check=True).count()
        context['allevents'] = filter(lambda x: not x.name.startswith("Задача дня"),
                                      Events.objects.filter(events__pk=self.kwargs['pk']).order_by('-date'))

        context['form'] = EventsForm()
        context['alldaytasks'] = filter(lambda x: x.name.startswith("Задача дня"),
                                        Events.objects.filter(events__pk=self.kwargs['pk']).order_by('-date'))
        context['rate_event'] = sum(
            map(lambda x: x.event_rate, Events.objects.filter(events__pk=self.kwargs['pk'], check=True)))
        return context

    def get(self, request, pk):
        if request.user.is_superuser or request.user.puples.pk == pk:
            return super().get(request, pk)
        return HttpResponseForbidden()

    def post(self, request, pk):
        form = EventsForm(request.POST, request.FILES)
        print(request.POST['date'],)
        if form.is_valid():
            form = form.save(commit=False)
            form.events_id = pk
            form.save()
            return redirect("/statistic/pupil/" + str(pk))
        return redirect(reverse_lazy("add_event", kwargs={'pk': pk}))


class CheckList(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    model = Events
    queryset = Events.objects.filter(check=False)
    template_name = "CheckList/check_list.html"
    login_url = '/login/'

    def get(self, request):
        if request.user.is_superuser:
            return super().get(request)
        else:
            return HttpResponseForbidden()

    def post(self, request):
        form = AddEventForm(request.POST)
        if form.is_valid() and request.POST["check"] == "True":
            a = Events.objects.get(pk=request.POST["id"])
            f = AddEventForm(request.POST, instance=a)
            f.save()
        elif request.POST["check"] == "False":
            b = Events.objects.get(pk=request.POST["id"])
            b.delete()
        return redirect("/check_list/")


class WorksView(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    queryset = Works.objects.all()
    template_name = "works/works.html"
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.puples.status == "APP":
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)



class IntensivView(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    queryset = Works.objects.all()
    template_name = "intensiv.html"
    raise_exception = True


class ApplicantView(HeaderNotificationsCounter, ListView):
    template_name = "applicant.html"
    queryset = Events.objects.all()


class PhotoGalleryView(HeaderNotificationsCounter, ListView):
    template_name = "photo_gallery.html"
    queryset = Events.objects.all()

    def post(self, request):
        print(request.POST)
        doc = DocxTemplate(settings.MEDIA_ROOT + "/files/templ.docx")
        data = request.POST
        context = {
            'name': f'{data["name"]}',
            'address': f'{data["address"]}',
            'number': f'{data["number"]}',
            'name_child': f'{data["name_child"]}',
            'date_br': f'{data["date_br"]}',
            'address_child': f'{data["address_child"]}',
            'profile': f'{data["profile"]}',
            'date_now': f'{dt.date.today().day}/0{dt.date.today().month}/{dt.date.today().year}'
        }

        doc.render(context)
        doc.save(settings.MEDIA_ROOT + f"/files/{data['class']}-{context['name_child']}.docx")
        return HttpResponse("<h1 style='text-align: center; font-family: Helvetica, serif;'>Заявление отправлено</h1>")


class SummerPracticeView(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    template_name = "summer_practice.html"
    queryset = SummerPractice.objects.all()
    login_url = '/login/'

    def post(self, request):
        req = request.POST
        check = bool(req["choise"])
        id_puple = str("|*" + req["id"] + "*|")
        list_id = SummerPractice.objects.get(id=request.POST['id_course'])
        if req["id"] not in list_id.id_registers and check:
            list_id.id_registers += id_puple
            list_id.save()
        elif req["id"] in list_id.id_registers and check:
            list_id.id_registers = list_id.id_registers.replace(id_puple, "")
            list_id.save()
        return redirect("/summer_practice/")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = str("|*" + str(self.request.user.id) + "*|")
        context["all"] = " ".join([SummerPractice.objects.all()[i].id_registers for i in range(3)])
        context["all2"] = " ".join([SummerPractice.objects.all()[i].id_registers for i in range(3, 6)])
        return context


class SummerPracticeAdminView(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    template_name = "summer_practice_admin.html"
    queryset = SummerPractice.objects.all()
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        all_puples = []
        for i in range(6):
            list_id = [int(j) for j in
                       SummerPractice.objects.all()[i].id_registers.rstrip('|*').lstrip('*|').split("*||*")]
            all_puples += list_id
            context[f"list{i}"] = [Puples.objects.get(user_id=k) for k in list_id]
            context[f"l{i}"] = len(list_id)
        all_id_user = {i.user_id for i in Puples.objects.all()}
        context["not_reg_puples"] = [Puples.objects.get(user_id=i) for i in all_id_user.difference(set(all_puples))]
        context["time"] = dt.datetime.now()
        return context


class NotificationsView(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    template_name = "notifications.html"
    queryset = Puples.objects.all()
    login_url = '/login/'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = sorted(list({people.get_status_display() for people in self.queryset}))
        return context

    def post(self, request):
        all_info = dict(request.POST)
        id_puples_send = [int(i) for i in all_info["checkbox_puple"]]
        email_list = [Puples.objects.get(user_id=i).email for i in id_puples_send]
        send_mail_to_applicant(*all_info["theme_letter"], *all_info["header_letter"], *all_info["text_letter"],
                               email_list)
        if "checkbox_telegram" in all_info:
            theme, text = str(*all_info["theme_letter"]), str(*all_info["text_letter"])
            all_mes = str(theme + "\n\n" + text)
            send_telegram(all_mes)
        return redirect("/notifications/")

class CheckClassv1(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    template_name = "check_class_v1.html"
    queryset = Puples.objects.all()
    login_url = '/login/'

    def post(self, request):
        print(request.POST)

        if "git" in request.POST and request.POST['git']:
            git = request.POST['git']
            user = Puples.objects.get(user=request.user.id)
            checker(git, user.surname + " " + user.name, user.email)
            return redirect("/check_class_v1/")
        else:
            return redirect("/check_class_v1/")

class CheckListv1(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    template_name = "check_list_v1.html"
    queryset = Puples.objects.all()
    login_url = '/login/'

    def post(self, request):
        if "git" in request.POST and request.POST['git']:
            git = request.POST['git']
            user = Puples.objects.get(user=request.user.id)
            checker_list_v1(git, user.surname + " " + user.name, user.email)
            return redirect("/check_list_v1/")
        else:
            return redirect("/check_list_v1/")


class ItWeek2021(ListView):
    template_name = "it_week2021/index.html"
    queryset = SummerPractice.objects.all()