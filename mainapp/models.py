from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField


class Puples(models.Model):
    STATUS_CHOICES = (
        ('ST10', 'Ученик 10 ИТ-класса'),
        ('ST11', 'Ученик 11 ИТ-класса'),
        ('APP', 'Кандидат в ИТ-класс'),
        ('TEACH', 'Учитель')
    )

    PROGRESS_CHOICES = (
        (0, '0'),
        (25, '25'),
        (50, '50'),
        (75, '75'),
        (100, '100'),
    )
    name = models.CharField("Имя", null=True, max_length=50)
    surname = models.CharField("Фамилия", null=True, max_length=100)
    rate = models.IntegerField("Рейтинг ученика", default=0)
    image = models.ImageField("Фотография профиля", blank=True, upload_to="puples_photo",
                              default="puples_photo/user-2.png")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default='',
                                verbose_name="Связь с таблицей пользователей")
    status = models.CharField("Статуc", choices=STATUS_CHOICES, default='ST10', max_length=30)
    applicant_first_result = models.FloatField("Результат первого этапа", blank=True, default=0)
    applicant_progress = models.IntegerField(verbose_name="Прогресс", choices=PROGRESS_CHOICES, default=0, blank=True)
    email = models.EmailField(verbose_name="Email", default="")
    phone = models.CharField(max_length=12, verbose_name="Телефон", default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"


class SummerPractice(models.Model):
    name = models.CharField("Название курса", max_length=200, default="")
    description = models.CharField("Описание курса", max_length=1000, default="")
    date = models.DateField("Дата", default="")
    time = models.TimeField("Время начала курса", default="")
    image = models.ImageField("Логотип курса", blank=True, upload_to="logo_practice",
                              default="puples_photo/user-2.png")
    id_registers = models.CharField(default="", verbose_name="ID учеников, кто дал правильный ответ", max_length=200,
                                    blank=True)

    class Meta:
        verbose_name = "Летняя практика"
        verbose_name_plural = "Летняя практика"

    def __str__(self):
        return self.name


class ApplicantAction(models.Model):
    date = models.DateField("Дата собеседования", default='')
    time = models.TimeField("Время собеседования", default='')
    url = models.URLField("Ссылка собесодования", default='')
    login = models.CharField("Идентификатор собеседования", max_length=30, default='')
    password = models.CharField("Пароль собеседования", max_length=50, default='')
    check = models.BooleanField(verbose_name="Подтверждение ученика", default=False)
    action_app = models.ForeignKey(Puples, on_delete=models.SET_NULL, null=True, verbose_name="Кандидат")

    class Meta:
        verbose_name = "Кандидаты"
        verbose_name_plural = "Кандидаты"


class Events(models.Model):
    date = models.DateField("Дата посещения")
    name = models.CharField("Название мероприятия", max_length=200)
    organization = models.CharField("Название организации", max_length=300)
    events = models.ForeignKey(Puples, verbose_name="Мероприятия", on_delete=models.SET_NULL, null=True)
    check = models.BooleanField(default=False)
    event_rate = models.IntegerField(default=0)
    verification_file = models.FileField(upload_to="verification_files/", null=True, verbose_name="Файл")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мероприятия"
        verbose_name_plural = "Мероприятия"


class Works(models.Model):
    date = models.DateField("Дата", null=True)
    theme = models.CharField("Название темы", max_length=200, default="")
    name = models.CharField("Название работы", max_length=200, default="")
    result = models.CharField(null=True, verbose_name="Результат", max_length=300, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Работы учеников"
        verbose_name_plural = "Работы учеников"


class DaysTask(models.Model):
    date = models.DateField("Дата", null=True)
    name_task = models.CharField("Название задачи", max_length=200)
    discription_task = HTMLField("Описание задачи")
    result = models.CharField(null=True, verbose_name="Результат", max_length=200)
    count_answer = models.IntegerField(default=0,
                                       verbose_name="Количество человек, которые могут решить задачу (указать отрицательное число)")
    id_answers = models.CharField(default="", verbose_name="ID учеников, кто дал правильный ответ", max_length=200,
                                  blank=True)

    def __str__(self):
        return f"Задача: \"{self.name_task}\""

    class Meta:
        verbose_name = "Задача дня"
        verbose_name_plural = "Задача дня"


class EventActive(models.Model):
    date = models.DateField("Дата", null=True)
    name = models.CharField("Название мероприятия", max_length=200)
    discription = models.TextField("Описание мероприятия")
    event_for_all = models.BooleanField(verbose_name="Показывать мероприятие всем", default=True, blank=False)
    link = models.URLField("Ссылка мероприятия", default='')

    class Meta:
        verbose_name = "Активные мероприятия"
        verbose_name_plural = "Активные мероприятия"

