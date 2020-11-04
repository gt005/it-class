import datetime

from django.db import models
from tinymce.models import HTMLField
from mainapp.models import Puples, Events
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class EducationLevel(models.Model):
    level_number = models.PositiveIntegerField(
        "Уровень группы задач",
        default=1
    )
    level_theme = models.CharField(
        "Тема, которая проходится на уровне",
        max_length=255
    )

    def __str__(self):
        return f"Задачи на тему '{self.level_theme}'. Уровень {self.level_number}"

    class Meta:
        verbose_name = "Уровень для задач"
        verbose_name_plural = "Уровни для задач"


class EducationTask(models.Model):
    """
    Задачи для решения.
    Пир(peer) - человек, которому пришла задача на проверку.
    """
    for_student = models.OneToOneField(Puples, on_delete=models.CASCADE, null=True, default=None, verbose_name="Предназначена для этого ученика")
    start_time = models.DateTimeField(verbose_name="Дата начала(открытие) задачи", auto_now_add=False)
    end_time = models.DateTimeField(verbose_name="Дата конца(закрытия) задачи", auto_now_add=False)
    task_level = models.ForeignKey(EducationLevel, verbose_name="Уровень задачи", default=1, on_delete=models.CASCADE)
    task_name = models.CharField(verbose_name="Название задания", max_length=200)
    description_task = models.TextField(verbose_name="Условие задачи")
    input_format = models.TextField(verbose_name="Формат ввода")
    output_format = models.TextField(verbose_name="Формат вывода")
    photo_1 = models.ImageField(verbose_name="Фото 1 для задачи", blank=True, upload_to="tasks_system_photos/")
    photo_2 = models.ImageField(verbose_name="Фото 2 для задачи", blank=True, upload_to="tasks_system_photos/")
    photo_3 = models.ImageField(verbose_name="Фото 3 для задачи", blank=True, upload_to="tasks_system_photos/")
    example_input_1 = models.TextField(verbose_name="Пример 1 ввод", blank=True)
    example_output_1 = models.TextField(verbose_name="Пример 1 вывод", blank=True)
    example_input_2 = models.TextField(verbose_name="Пример 2 ввод", blank=True)
    example_output_2 = models.TextField(verbose_name="Пример 2 вывод", blank=True)
    example_input_3 = models.TextField(verbose_name="Пример 3 ввод", blank=True)
    example_output_3 = models.TextField(verbose_name="Пример 3 вывод", blank=True)

    def __str__(self):
        return f"{self.task_name}. Уровень {self.task_level.level_number}"

    class Meta:
        verbose_name = "Задача для решения"
        verbose_name_plural = "Задачи для решения"


class CheckedEducationTask(models.Model):
    """Задача, которую уже отправили на проверку или которая прошла проверку"""
    original_task = models.ForeignKey(
        EducationTask,
        verbose_name="Оригинал задачи",
        on_delete=models.SET_NULL,
        null=True
    )
    solved_user = models.ForeignKey(
        Puples, verbose_name="Человек, отправивший на проверку",
        on_delete=models.CASCADE
    )
    task_code = models.TextField(
        verbose_name="Решение задачи в виде кода"
    )
    solution_time = models.DateTimeField(
        "Время, когда принято решение",
        auto_now_add=True
    )
    task_programming_language = models.CharField(
        "Язык программирования, на котором написана задача",
        max_length=32,
        default="Python 3.7.3"
    )
    first_peer = models.ForeignKey(
        Puples,
        verbose_name="Peer 1",
        related_name="Peer_1",
        on_delete=models.SET_NULL,
        null=True
    )
    first_peer_mark = models.PositiveIntegerField(
        verbose_name="Оценка peer 1",
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    second_peer = models.ForeignKey(
        Puples,
        verbose_name="Peer 2",
        related_name="Peer_2",
        on_delete=models.SET_NULL,
        null=True
    )
    second_peer_mark = models.PositiveIntegerField(
        verbose_name="Оценка peer 2",
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    contest_token = models.CharField(
        verbose_name="Токен для Яндекс.Контест",
        max_length=255
    )
    system_mark = models.PositiveIntegerField(
        verbose_name="Оценка Яндекс.Контест",
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    result_summ_mark = models.PositiveIntegerField(
        verbose_name="Общий итог всех оценок",
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(300)]
    )

    def get_solution_time(self) -> str:
        """ Возвращает время в формате без time zone """
        return self.solution_time.strftime("%d %b %Y, %H:%M:%S")

    def __str__(self):
        return f"{self.original_task.task_name}. Уровень {self.original_task.task_level.level_number}"

    class Meta:
        verbose_name = "Решенная задача"
        verbose_name_plural = "Решенные задачи"

