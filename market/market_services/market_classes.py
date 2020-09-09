from typing import Union
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from market.models import MarketProduct
from market.market_services.market_operations import get_correct_form_of_points_number_name, buying_product_from_market


class ShoppingCart(object):
    """ Корзина с товрами """

    def __init__(self, request):
        """ Создание корзины """

        self.request = request
        self.session = request.session
        cart = self.session.get(settings.SHOPPING_CART_SESSION_ID)
        if not cart:  # Если никогда не было
            cart = self.session[settings.SHOPPING_CART_SESSION_ID] = {}
        self.shopping_cart = cart

    def __iter__(self) -> dict:
        """
        Перебор элементов корзины и получение объектов товаров из базы данных.
        Создание итератора словарей {'product': MarketProduct, 'amount': int}
        """
        self._delete_missing_products()

        for product in self.shopping_cart:
            yield {
                "product": MarketProduct.objects.get(id=int(product)),
                "amount": self.shopping_cart[product]["amount"]
            }

    def len(self):
        """ Количество элементов в корзине """
        self._delete_missing_products()
        return len(self.shopping_cart)

    def get_shopping_cart_list(self) -> list:
        """ Возвращает список объектов продуктов из корины """
        self._delete_missing_products()
        return [MarketProduct.objects.get(id=int(product)) for product in self.shopping_cart]

    def add(self, product_id: str, amount:int=1) -> str:
        """
         Добавляет предмет в корзину с заданным количеством.
         :param str product_id: Id продукта из таблицы MarketProduct
         :param int amount: Задает количество продуктов
         :return: Строка с ошибкой или строка "success", если продукт успешно добавился.

        """
        product_id = str(product_id)
        try:
            amount = int(amount)
        except ValueError:
            return "Некорректное значение количества товара"

        if amount <= 0:
            return "Неверное количество товара"

        try:
            MarketProduct.objects.get(id=int(product_id))
        except ValueError:
            return "Некорректное значение id продукта"
        except ObjectDoesNotExist:
            return "Такого объекта не существует"

        self.shopping_cart[product_id] = {"amount": amount}
        self.save()
        return "success"

    def remove(self, product_id: str) -> str:
        """ Удаляет продукт из корзины """
        product_id = str(product_id)
        if product_id in self.shopping_cart:
            del self.shopping_cart[product_id]
            self.save()
            return "success"
        return "Такой товар в корзине не найден"

    def get_total_price(self, add_points_name: bool=True) -> Union[str, int]:
        """
        Считает общую сумму корзины
        :param bool add_points_name: Если True, то возвращает строку со словом 'баллы' в правильной форме
        """
        self._delete_missing_products()
        total_price = 0
        for product in self.shopping_cart:
            product_from_db = MarketProduct.objects.get(id=int(product))
            total_price += (product_from_db.price * self.shopping_cart[product]["amount"])

        if add_points_name:
            return f"{str(total_price)} {get_correct_form_of_points_number_name(total_price)}"
        return total_price

    def buy_products_from_cart(self) -> str:
        """
        Совершает покупку всех товаров в корзине.
        Делает проверку на наличие средств на покупку, проверку на наличие количества товара в магазине.
        """
        if self.request.user.puples.rate < self.get_total_price(add_points_name=False):
            return "Не хватает денег на покупку"

        for product in self:  # Проверка на наличие каждого товара и в определенном количестве
            if MarketProduct.objects.get(id=product["product"].id).remained_amount < product["amount"]:
                return "Какой-то товар закончился или нет столько товара"

        for product in self:  # Покупка каждого товара
            for amount_of_products in range(product["amount"]):
                buying_product_from_market(product["product"].id, request=self.request)

        self.clear()
        return "Success"

    def clear(self):
        """ Очистка корзины """
        self.shopping_cart = {}
        self.session[settings.SHOPPING_CART_SESSION_ID] = {}
        self.save()

    def save(self) -> None:
        """ Сохранение изменений """
        self.session.modified = True

    def _delete_missing_products(self) -> None:
        """
        Удаляет продукты из корзины, которых нет в базе данных.
        Такое может произойти, если товар добавлен в корзину, а из бд удалили.
        """
        products_to_delete = []  # Те продукты, которые есть в корзине, но уже удалены из магазина
        for product in self.shopping_cart:
            try:
                MarketProduct.objects.get(id=int(product))
            except ObjectDoesNotExist:
                products_to_delete.append(product)

        for product_to_delete in products_to_delete:
            self.remove(product_to_delete)

        self.save()
