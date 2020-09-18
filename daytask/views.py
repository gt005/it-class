from django.shortcuts import render
from mainapp.addons_python.views_addons_classes import HeaderNotificationsCounter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, View
from .models import Tasks
from mainapp.models import Events, Puples
import datetime as dt
from pymorphy2 import MorphAnalyzer
from django.shortcuts import redirect

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


    def post(self, request):
        now_task = Tasks.objects.get(date=dt.datetime.now().date(), status_task=self.request.user.puples.status)
        if request.POST["result"] == now_task.result:
            Events.objects.create(name=f"Задача дня \"{now_task.name}\"", date=dt.date.today(),
                                  organization="ГБОУ Школа 1158",
                                  events=Puples.objects.get(user=request.user.id),
                                  event_rate=5, check=True,
                                  verification_file="123.jpg")
            now_task.count_answer += 1
            now_task.id_puple_correct_answers += " " + str(Puples.objects.get(user=request.user.id).user.id) + " "
            now_task.tries_list += " " + str(Puples.objects.get(user=request.user.id).user.id) + " "
            now_task.save()
            return redirect("/daytask")
        now_task.tries_list += " " + str(Puples.objects.get(user=request.user.id).user.id) + " "
        now_task.save()
        return redirect("/daytask")


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["task"] = Tasks.objects.get(date=dt.datetime.now().date(), status_task=self.request.user.puples.status)
        except:
            context["task"] = None
        context["end_time"] = self.time_end_task(context["task"])
        try:
            made_tries = len(list(filter(lambda x: x == self.request.user.id, [int(i) for i in context['task'].tries_list.split()])))
            context['tries'] = made_tries
            if context['task'].tries - made_tries > 0:
                context["button"] = f"Отправить (осталось {context['task'].tries - made_tries} {self.convert_words('попытка', context['task'].tries - made_tries)})"
            elif context['task'].tries == -1:
                context["button"] = "Отправить решение"
            else:
                context["button"] = ""
        except:
            pass
        return context

