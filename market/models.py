from django.db import models
from mainapp.models import Puples, Events


class MarketProduct(models.Model):
    """ Товары, которые выставлены на продажу (если товар закончился, запись НЕ удаляется) """

    product_name = models.CharField(verbose_name="Название товара", max_length=200)
    product_size = models.CharField(verbose_name="Размер товара", default="Стандарт", max_length=200)
    product_color = models.CharField(verbose_name="Цвет товара", default="Не указан", max_length=200)
    product_photo = models.ImageField("Фотография товара", upload_to="products_photo/", blank=True)
    remained_amount = models.PositiveIntegerField("Количество оставшегося товара", null=False)
    price = models.PositiveIntegerField("Цена товара", null=False)

    def __str__(self):
        return f"{self.product_name}\t-\tразмер {self.product_size}\t-\tцвет {self.product_color}"

    def plural_amount_name(self) -> str:
        """ Возвращает верное слово (Баллов/Балла/Балл) для правильного написания """
        if 10 <= (self.price % 100) <= 20 or self.price % 10 == 0 or 5 <= self.price % 10 <= 9:
            return "Баллов"
        elif self.price % 10 == 1:
            return "Балл"
        return "Балла"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class BoughtProduct(models.Model):
    """
    Если товар куплен, то он попадает в эту таблицу с привязкой к пользователю, который его купил.
    Также, купленный товар привязан к основному товару из таблицы MarketProduct, который выставлен на продажу
    """

    customer = models.ForeignKey(Puples, verbose_name="Покупатель товара", on_delete=models.SET_NULL, null=True)
    main_product = models.ForeignKey(MarketProduct, verbose_name="Ссылка на основной товар", on_delete=models.CASCADE)
    connected_event = models.ForeignKey(Events, verbose_name="Ссылка на Event с этой покупкой", on_delete=models.CASCADE, default=None)
    bought_date = models.DateField("Дата покупки", auto_now_add=True)
    given_date = models.DateField("Дата выдачи товара", null=True)
    given = models.BooleanField("Выдан ли товар покупателю", default=False)

    def __str__(self):
        return f"{self.main_product}"

    class Meta:
        verbose_name = "Заказ/купленный товар"
        verbose_name_plural = "Заказы и купленные товары"
