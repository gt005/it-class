from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from pymorphy2 import MorphAnalyzer
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, JsonResponse
from random import randint, choice
from django.http import HttpResponse
from django.template import Context, loader
import datetime
import json

from mainapp.addons_python.notifications import send_mail_to_admin
from mainapp.addons_python.views_addons_classes import HeaderNotificationsCounter
from mainapp.models import Events, Puples
from .models import Task, Variant
from django.template.defaulttags import register

# Create your views here.

class ExamPrepMain(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    template_name = "exam_prep/exam_prep_main.html"
    queryset = Task
    login_url = '/login/'

    def create_str_tasks(self):
        s = dict()
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27]:
            try:
                number_in_ege_bank = [i.number_task for i in Task.objects.filter(number_ege=i)]
                if not number_in_ege_bank:
                    number_in_ege_bank = [1]
            except:
                number_in_ege_bank = [1]
            s[i] = choice(number_in_ege_bank)
        return json.dumps(s)

    def post(self, request):
        while 1:
            num_var = randint(1, 100000000)
            if num_var not in [i.id_var for i in Variant.objects.all()]:
                break
        ans = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [],
               15: [], 16: [], 17: [], 18: [], 19: [], 22: [], 23: [], 24: [], 25: [], 26: [], 27: []}
        p = Variant(id_var=num_var,
                    tasks=self.create_str_tasks(),
                    puples=Puples.objects.get(user_id=request.user.id),
                    date=datetime.datetime.now().date(),
                    answers=json.dumps(ans))
        p.save()
        return redirect("/exam_prep/" + str(request.user.id) + "_" + str(num_var) + "?number_ege=1")

    def get(self, request):
        cur_var = Variant.objects.filter(puples=Puples.objects.get(user_id=request.user.id), end=False)
        try:
            cur_var = cur_var[len(cur_var) - 1]
            if datetime.datetime.now().date() <= cur_var.date + datetime.timedelta(days=7):
                return redirect("/exam_prep/" + str(request.user.id) + "_" + str(cur_var.id_var) + "?number_ege=1")
            else:
                cur_var.end = True
                cur_var.save()
                return redirect("/exam_prep/")
        except:
            pass
        return super().get(request)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ege_convert = {0: 0, 1: 7, 2: 14, 3: 20, 4: 27, 5: 34, 6: 40, 7: 43, 8: 46, 9: 48, 10: 51, 11: 54, 12: 56,
                       13: 59, 14: 62, 15: 64, 16: 67, 17: 70, 18: 72, 19: 75, 20: 78, 21: 80, 22: 83, 23: 85, 24: 88,
                       25: 90, 26: 93, 27: 95, 28: 98, 29: 100}
        all_variants = Variant.objects.filter(puples=Puples.objects.get(user_id=self.request.user.id), end=True)
        ege_vars = all_variants
        all_count = all_variants.count()
        if all_count >= 10:
            ege_vars = ege_vars[all_count-10:all_count]
        all_ok_score_for_all_vars = []
        all_ege_score_for_all_vars = []
        for var in ege_vars:
            ok_ans_var = 0
            dict_tmp = json.loads(var.answers)
            for taks in dict_tmp:
                if dict_tmp[taks]:
                    if dict_tmp[taks][-1][-3] == "OK":
                        ok_ans_var += 1
            all_ok_score_for_all_vars.append(ok_ans_var)
            all_ege_score_for_all_vars.append(ege_convert[ok_ans_var])
        ege_level = 0
        if len(all_ege_score_for_all_vars):
            ege_level = sum(all_ege_score_for_all_vars)//len(all_ege_score_for_all_vars)
        context["ege_level"] = ege_level
        context["variants"] = all_variants
        return context


class ExamPrepView(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    template_name = "exam_prep/exam_prep.html"
    queryset = Task
    login_url = '/login/'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        number_ege_cur = int(self.request.GET["number_ege"])
        current_variant_user = list(Variant.objects.filter(puples=Puples.objects.get(user_id=self.request.user.id)))[-1]
        list_tasks = json.loads(current_variant_user.tasks)
        dict_ans = json.loads(current_variant_user.answers)
        try:
            last_answer = dict_ans[str(number_ege_cur)][-1][1]
        except:
            last_answer = ""
        context["list_answer"] = [int(i) for i in dict_ans if dict_ans[i]]
        context["last_answer"] = last_answer
        context["active_num"] = number_ege_cur
        context["tasks"] = Task.objects.get(number_ege=number_ege_cur, number_task=list_tasks[str(number_ege_cur)])
        context["line_num"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26,
                               27]
        return context

    def post(self, request, id_var, task_num=1):
        print(request.POST)
        id_p, id_v = map(int, id_var.split("_"))
        cur_ans = Variant.objects.get(id_var=id_v)
        number_ege_cur = int(self.request.GET["number_ege"])
        if "task_problem" in request.POST:
            disc_problem = request.POST["task_problem"]
            id_task = request.POST["id_task"]
            try:
                send_mail_to_admin(f"Проблема с заданием",
                                   "",
                                   f"Задание №{id_task} <br>Описание проблемы: {disc_problem}",
                                   ["ibkov@yandex.ru", ])
            except:
                pass
            return redirect(f"/exam_prep/{id_var}?number_ege={number_ege_cur}")
        if "end_var" in request.POST:
            cur_ans.end = True
            cur_ans.save()
            return redirect(f"/exam_prep/{id_var}/result")
        input_answer = request.POST["answer"]
        current_variant_user = list(Variant.objects.filter(puples=Puples.objects.get(user_id=self.request.user.id)))[-1]
        list_tasks = json.loads(current_variant_user.tasks)
        cur_task = Task.objects.get(number_ege=number_ege_cur, number_task=list_tasks[str(number_ege_cur)])
        correct_answer = cur_task.result
        task_id = cur_task.id_task
        dict_ans = json.loads(current_variant_user.answers)
        if input_answer.lower().strip() == correct_answer.lower().strip():
            dict_ans[str(number_ege_cur)].append((str(datetime.datetime.now()), input_answer, "OK", task_id, correct_answer))
        else:
            dict_ans[str(number_ege_cur)].append((str(datetime.datetime.now()), input_answer, "WA", task_id, correct_answer))
        cur_ans.answers = json.dumps(dict_ans)
        cur_ans.save()
        return redirect(f"/exam_prep/{id_var}?number_ege={number_ege_cur}")

    def get(self, request, id_var, task_num=1):
        id_puple, id_var = map(int, id_var.split('_'))
        try:
            if Variant.objects.get(id_var=id_var).end:
                return redirect(f"/exam_prep/{id_var}/result")
            if Variant.objects.get(id_var=id_var).date + datetime.timedelta(days=7) < datetime.datetime.now().date() \
                    or request.user.id != id_puple:
                return HttpResponseForbidden()
        except:
            return HttpResponseForbidden()
        return super().get(request)


class ExamPrepResult(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    template_name = "exam_prep/exam_prep_result.html"
    queryset = Variant
    login_url = '/login/'

    def get(self, request, id_var, task_num=1):
        id_puple, id_var = map(int, id_var.split('_'))
        cur_var = Variant.objects.get(id_var=id_var)
        if not cur_var.end:
            return redirect(f"/exam_prep/")
        return super().get(request)

    @register.filter
    def get_value(dictionary, key):
        return dictionary.get(key)

    def get_context_data(self, *args, object_list=None, **kwargs):
        id_puple, id_var = map(int, self.request.path.split('/')[-2].split("_"))
        context = super().get_context_data(**kwargs)
        cur_var = Variant.objects.get(id_var=id_var)
        all_answers = cur_var.answers
        dict_all_ans = json.loads(all_answers)
        only_last_answers = {}
        tryes = {}
        count_right = 0
        for i in dict_all_ans:
            tryes[i] = {"try":0,"ans":"WA"}
            if dict_all_ans[i]:
                tryes[i]["try"] = len(dict_all_ans[i])
                only_last_answers[i] = dict_all_ans[i][-1]
                if dict_all_ans[i][-1][2] == "OK":
                    tryes[i]["ans"] = "OK"
                    count_right += 1
            else:
                only_last_answers[i] = []
        ege_convert = {0: 0, 1: 7, 2: 14, 3: 20, 4: 27, 5: 34, 6: 40, 7: 43, 8: 46, 9: 48, 10: 51, 11: 54, 12: 56,
                       13: 59, 14: 62, 15: 64, 16: 67, 17: 70, 18: 72, 19: 75, 20: 78, 21: 80, 22: 83, 23: 85, 24: 88,
                       25: 90, 26: 93, 27: 95, 28: 98, 29: 100}
        context["one_try_task"] = len([i for i in tryes if tryes[i]["ans"] == "OK" and tryes[i]["try"] == 1])
        context["tryes"] = tryes
        context["variant"] = only_last_answers
        context["count_right"] = count_right
        context["ege_level"] = ege_convert[count_right]
        context["var_id"] = id_var

        return context
