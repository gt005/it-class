import datetime as dt

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from pymorphy2 import MorphAnalyzer

from mainapp.addons_python.views_addons_classes import HeaderNotificationsCounter
from mainapp.models import Events, Puples
from .forms import TaskForm
from .models import Tasks


class DayTaskView(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    template_name = "daytask/daytask.html"
    queryset = Tasks
    login_url = '/login/'

    def time_end_task(self, task):
        if task:
            hh, mm = 23, 59
            a = dt.datetime.now().time().hour
            b = dt.datetime.now().time().minute
            hh -= a
            mm -= b
            a = MorphAnalyzer()
            hour = a.parse('час')[0]
            minute = a.parse('минута')[0]
            return f"До конца задачи осталось {hh} {hour.make_agree_with_number(hh).word} \
                {mm} {minute.make_agree_with_number(hh).word}"
        return ""

    def convert_words(self, word, number):
        a = MorphAnalyzer()
        conv_word = a.parse(word)[0]
        return conv_word.make_agree_with_number(number).word

    def tries_list_with_time(self, str):
        return [(int(i.split("|")[0]), i.split("|")[1]) for i in str.split()]

    def post(self, request):
        now_task = Tasks.objects.get(date=dt.datetime.now().date(), status_task=self.request.user.puples.status)
        self.made_tries = len(list(filter(lambda x: x == self.request.user.id,
                                          [i[0] for i in self.tries_list_with_time(now_task.tries_list)])))
        if request.POST["result"] == now_task.result and self.made_tries < now_task.tries:
            Events.objects.create(name=f"Задача дня \"{now_task.name}\"", date=dt.date.today(),
                                  organization="ГБОУ Школа 1158",
                                  events=Puples.objects.get(user=request.user.id),
                                  event_rate=now_task.score // (len(now_task.id_puple_correct_answers.split()) + 1),
                                  check=True, verification_file="123.jpg")
            now_task.id_puple_correct_answers += " " + str(Puples.objects.get(user=request.user.id).user.id) + " "
            now_task.tries_list += " " + str(Puples.objects.get(user=request.user.id).user.id) + "|" + str(
                dt.datetime.now().strftime("%H:%M:%S")) + " "
            now_task.save()
            return redirect("/daytask")
        if self.made_tries >= now_task.tries:
            return redirect("/daytask")
        now_task.tries_list += " " + str(Puples.objects.get(user=request.user.id).user.id) + "|" + str(
            dt.datetime.now().strftime("%H:%M:%S")) + " "
        now_task.save()
        return redirect("/daytask")

    def type_tasks(self, day):
        all_types_tasks = {"active": [(i, [Puples.objects.get(user=j) for j in i.id_puple_correct_answers.split()]) \
                                      for i in Tasks.objects.filter(date=day)]}
        all_types_tasks["last"] = [(i, [Puples.objects.get(user=j) for j in i.id_puple_correct_answers.split()]) \
                                   for i in Tasks.objects.filter(date__lt=day)]
        all_types_tasks["fiture"] = [(i, [Puples.objects.get(user=j) for j in i.id_puple_correct_answers.split()]) \
                                     for i in Tasks.objects.filter(date__gt=day)]
        return all_types_tasks

    def get_list_solved_task(self, x):
        return [(Puples.objects.get(user_id=i).surname, Puples.objects.get(user_id=i).name) for i in x]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["tasks_active_teacher"] = self.type_tasks(dt.datetime.now().date())["active"]
            context["tasks_last_teacher"] = self.type_tasks(dt.datetime.now().date())["last"]
            context["tasks_fiture_teacher"] = self.type_tasks(dt.datetime.now().date())["fiture"]
            context["list_names_success"] = ""
            context["task"] = Tasks.objects.get(date=dt.datetime.now().date(),
                                                status_task=self.request.user.puples.status)
        except:
            context["task"] = None
        context["end_time"] = self.time_end_task(context["task"])
        try:
            self.made_tries = len(list(filter(lambda x: x == self.request.user.id,
                                         [i[0] for i in self.tries_list_with_time(context['task'].tries_list)])))
            if self.made_tries and self.made_tries != context["task"].tries:
                context['mistake'] = "Ответ неверный"
            context['tries'] = self.made_tries
            if context['task'].tries - self.made_tries > 0:
                context["button"] = f"Отправить (осталось {context['task'].tries - self.made_tries} \
                {self.convert_words('попытка', context['task'].tries - self.made_tries)})"
            elif context['task'].tries == -1:
                context["button"] = "Отправить решение"
            else:
                context["button"] = ""
        except:
            pass
        try:
            context["id_puple_correct_answers"] = [int(i) for i in context["task"].id_puple_correct_answers.split()]
            context["count_right_answers"] = len(context["id_puple_correct_answers"])
            context['list_name_right_answers'] = self.get_list_solved_task(context['id_puple_correct_answers'])
        except:
            context["id_puple_correct_answers"] = None
        return context


class DayTaskAddView(HeaderNotificationsCounter, LoginRequiredMixin, CreateView):
    template_name = "daytask/daytask_add.html"
    queryset = Tasks
    login_url = '/login/'
    form_class = TaskForm

    def check_date_class_not_in_tasks(self, request):
        dd, mm, yy = map(int, request.POST["date"].split("."))
        if dt.date(yy, mm, dd) < dt.datetime.now().date():
            self.errors["last_date"] = "Вы не можете создать задачу на прошедшую дату."
            return False
        status_POST = request.POST["status_task"]
        self.errors['same_task'] = "Задача на указанную дату уже существует, укажите другую дату."
        return not any(i[0] == dt.date(yy, mm, dd) and i[1] == status_POST for i in [(task.date, task.status_task) \
                                                                                     for task in Tasks.objects.all()])

    def post(self, request):
        form = TaskForm(request.POST)
        self.errors = {'form': form}
        if form.is_valid() and self.check_date_class_not_in_tasks(request):
            form = form.save(commit=False)
            form.save()
            return redirect("/daytask")
        return render(request, 'daytask/daytask_add.html', self.errors)


class DayTaskShowView(DayTaskView):
    template_name = "daytask/daytask_show.html"
    queryset = Tasks
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = Tasks.objects.get(id=int(self.kwargs['id']))
        return context

    def __init__(self):
        super().__init__()


class DayTaskEditView(DayTaskAddView):
    template_name = "daytask/daytask_edit.html"
    queryset = Tasks
    login_url = '/login/'
    form_class = TaskForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = Tasks.objects.get(id=int(self.kwargs['id']))
        yy, mm, dd = map(str, str(context['task'].date).split("-"))
        context['date'] = dd + "." + mm + "." + yy
        context['form'] = TaskForm(
            initial={"name": context['task'].name,
                     "discription_task": context['task'].discription_task,
                     "status_task": context['task'].status_task,
                     "result": context['task'].result,
                     "count_answer": context['task'].count_answer,
                     "score": context['task'].score,
                     "tries": context['task'].tries})
        return context

    def post(self, request, id):
        form = TaskForm(request.POST)
        self.errors = {'form': form}
        yy, mm, dd = map(str, str(Tasks.objects.get(id=id).date).split("-"))
        self.str_date = dd + "." + mm + "." + yy
        if form.is_valid() and (
                request.POST['date'] == self.str_date or self.check_date_class_not_in_tasks(request)):
            a = Tasks.objects.get(id=id)
            form = TaskForm(request.POST, instance=a)
            form.save()
            return redirect("/daytask")
        print(self.errors)
        return render(request, 'daytask/daytask_edit.html', self.errors)
