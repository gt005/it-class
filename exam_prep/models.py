from django.db import models
from tinymce.models import HTMLField
from mainapp.models import Puples

class Task(models.Model):
    id_task = models.AutoField(primary_key=True)
    number_ege  = models.IntegerField("Номер ЕГЭ")
    number_task = models.IntegerField("Номер задания", default='0')
    discription_task_text = models.TextField("Условие задачи", null=True)
    discription_task = models.ImageField("Условие задачи", blank=True, upload_to="puples_photo",
                              default="puples_photo/user-2.png")
    url = models.CharField("Ссылка на файл к заданию", default='', blank=True, max_length=200)
    grade_task = models.IntegerField("Сложность")
    result = models.CharField(null=True, verbose_name="Правильный ответ на задачу", max_length=200)


    def __str__(self):
        return f"Задача ЕГЭ №:{self.number_ege}"

    class Meta:
        verbose_name = "Задания ЕГЭ"
        verbose_name_plural = "Задания ЕГЭ"


class Variant(models.Model):
    id_var = models.IntegerField("Номер варианта")
    tasks = models.CharField(null=True, verbose_name="Номера заданий варианта", max_length=500)
    puples = models.ForeignKey(Puples, verbose_name="Ученик", on_delete=models.SET_NULL, null=True)
    date = models.DateField("Дата начала варианта", default="2000-01-01")
    answers = models.TextField("Ответы ученика", default="", null=True, blank=True)
    end = models.BooleanField("Вариант завершен", default=False)

    class Meta:
        verbose_name = "Варианты"
        verbose_name_plural = "Варианты"

    def __str__(self):
        return f"Задача: \"{self.puples.surname}\""
