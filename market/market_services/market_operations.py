import datetime
from django.core.exceptions import ObjectDoesNotExist
from mainapp.models import Events
from market.models import MarketProduct, BoughtProduct
from pymorphy2 import MorphAnalyzer


def buying_product_from_market(product_id_for_buy: int, request) -> str:
    """
    Производит валидацию данных. Если все данные верны, то происходит покупка.
    Покупка - списание средств и добавление продукта в таблицу с купленными товарами.

    Возвращает 'Success', если средства списали у покупателя и добавился заказ
    на продукт в таблицу BoughtProduct, иначе возвращается сообщение с ошибкой.
    """
    try:
        if int(product_id_for_buy) > 0:
            product_from_db = MarketProduct.objects.get(id=product_id_for_buy)
    except ValueError:
        return "Некорректное значение продукта"
    except ObjectDoesNotExist:
        return "Такого объекта не существует"

    if product_from_db.remained_amount == 0:
        return "Такого товара больше не осталось"

    if request.user.puples.rate < product_from_db.price:
        return "Недостаточно средств"

    new_buy_event = Events(
        date=datetime.date.today(),
        name=f"Покупка: {product_from_db}",
        organization="ГБОУ школа 1158",
        events=request.user.puples,
        check=True,
        event_rate=-product_from_db.price,
    )

    new_buy_event.save()

    bough_product = BoughtProduct(
        customer=request.user.puples,
        main_product=product_from_db,
        connected_event=new_buy_event
    )

    bough_product.save()

    product_from_db.remained_amount -= 1
    product_from_db.save()

    request.user.puples.rate -= product_from_db.price
    request.user.puples.save()

    return "Success"


def give_product_to_customer(product_to_give_id: int, request) -> None:
    """ Подтверждает выдачу товара ученику. Может подтвердить только admin """
    product_to_give = BoughtProduct.objects.get(id=product_to_give_id)
    product_to_give.given_date = datetime.date.today()
    product_to_give.given = True
    product_to_give.save()


def cancel_given_product_to_customer(product_to_cancel_id: int, request) -> None:
    """
    Отменяет заказ на товар, возвращая средства покупателю и количество товара.
    Может подтвердить только admin.
    """
    product_to_cancel = BoughtProduct.objects.get(id=product_to_cancel_id)
    product_to_cancel.main_product.remained_amount += 1
    product_to_cancel.customer.rate += product_to_cancel.main_product.price

    product_to_cancel.main_product.save()
    product_to_cancel.customer.save()
    product_to_cancel.connected_event.delete()
    product_to_cancel.delete()


def get_correct_form_of_points_number_name(number: int) -> str:
    """ Возвращает верное слово (Баллов/Балла/Балл) для правильного написания """
    if not isinstance(number, int):  # Ввелось не число
        return "Балл"

    analysis = MorphAnalyzer().parse("Балл")[0]
    return analysis.make_agree_with_number(number).word
