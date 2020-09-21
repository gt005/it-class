from django.db import models
from tinymce.models import HTMLField
from mainapp.models import Puples, Events


class EducationTask(models.Model):
    """
    Задачи для решения.
    Пир(peer) - человек, которому пришла задача на проверку.
    """
    date = models.DateField("Дата", null=True)
    task_name = models.CharField(verbose_name="Название задания", max_length=200)
    discription_task = HTMLField("Описание задачи")
    visibility = models.BooleanField(verbose_name="Видимость задачи для учеников", default=False)


class CheckedEducationTask(models.Model):
    original_task = models.ForeignKey(EducationTask, verbose_name="Оригинал задачи", on_delete=models.SET_NULL, null=True)
    solved_user = models.ForeignKey(Puples, verbose_name="Человек, отправивший на проверку", on_delete=models.CASCADE)
    task_code = models.TextField(verbose_name="Решение задачи в виде кода")
    first_peer = models.ForeignKey(Puples, verbose_name="Пир 1", on_delete=models.SET_NULL, null=True)
    first_peer_report = models.TextField(verbose_name="Комментарии пира в определенном формате")
    first_peer_mark = count_answer = models.PositiveIntegerField(verbose_name="Оценка пира 1", null=True)
    second_peer = models.ForeignKey(Puples, verbose_name="Пир 2", on_delete=models.SET_NULL, null=True)

    contest_token = models.CharField(verbose_name="Токен для Яндекс.Контест", max_length=200)



