from django.db import models
from tinymce.models import HTMLField


class Tasks(models.Model):
    STATUS_CHOICES = (
        ('ST10', '10 класс'),
        ('ST11', '11 класс'),
    )
    date = models.DateField("Дата задачи", null=True)
    name = models.CharField("Название задачи", null=True, max_length=150)
    discription_task = HTMLField("Условие задачи")
    status_task = models.CharField("Выберите класс", choices=STATUS_CHOICES, default='ST10', max_length=30)
    result = models.CharField(null=True, verbose_name="Правильный ответ на задачу", max_length=200)
    count_answer = models.IntegerField(default=2,
                                       verbose_name="Количество человек, которые могут решить задачу")
    score = models.IntegerField("Максимальный балл за задачу", default=5)
    tries = models.IntegerField(default=-1, verbose_name="Количество попыток ответа на каждого ученика (-1 - бесконечно)")
    tries_list = models.CharField(default="", verbose_name="ID учеников, совершившие попытку",
                                                max_length=200,
                                                blank=True)
    id_puple_correct_answers = models.CharField(default="", verbose_name="ID учеников, кто дал правильный ответ",
                                                max_length=200,
                                                blank=True)

    def __str__(self):
        return f"Задача: \"{self.name}\""

    class Meta:
        verbose_name = "Задача дня"
        verbose_name_plural = "Задача дня"
