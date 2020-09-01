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
    rate = models.PositiveIntegerField("Рейтинг ученика", default=0)
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


class MarketProduct(models.Model):
    """ Товары, которые выставлены на продажу (если товар закончился, запись НЕ удаляется) """

    product_name = models.CharField(verbose_name="Название товара", max_length=200)
    product_size = models.CharField(verbose_name="Размер товара", default="Стандарт", max_length=200)
    product_color = models.CharField(verbose_name="Цвет товара", default="Не указан", max_length=200)
    product_photo = models.ImageField("Фотография товара", upload_to="products_photo/", blank=True)
    remained_amount = models.PositiveIntegerField("Количество оставшегося товара", null=False)
    price = models.PositiveIntegerField("Цена товара", null=False)

    def __str__(self):
        return f"{self.product_name}\t-\t{self.product_size}"

    def plural_amount_name(self):
        """ Возвращает верное слово (Баллов/Балла/Балл) для правильного написания """
        if 10 <= self.price <= 20 or self.price % 10 == 0 or 5 <= self.price % 10 <= 9:
            return "Баллов"
        elif self.price % 10 == 1:
            return "Балл"
        return "Балла"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class BoughtProduct(models.Model):
    """ Если товар куплен, то он попадает в эту таблицу с привязкой к пользователю, который его купил.
        Также, купленный товар привязан к основному товару из таблицы MarketProduct, который выставлен на продажу
    """

    customer = models.ForeignKey(Puples, verbose_name="Покупатель товара", on_delete=models.SET_NULL, null=True)
    main_product = models.ForeignKey(MarketProduct, verbose_name="Ссылка на основной товар", on_delete=models.CASCADE)
    bought_date = models.DateField("Дата покупки", auto_now_add=True)
    given = models.BooleanField("Выдан ли товар покупателю", default=False)

    def __str__(self):
        return f"{self.main_product}"

    class Meta:
        verbose_name = "Купленный товар"
        verbose_name_plural = "Купленные товары"
