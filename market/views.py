from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from .models import MarketProduct, BoughtProduct
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist


class MainMarketPage(LoginRequiredMixin, ListView):
    """ Страница с каталогом товаров магазина """
    template_name = "market/main_market_page.html"
    model = MarketProduct
    login_url = "/login/"

    def post(self, request):
        return redirect(f"/market/market_success/?message={_buying_product_from_market(request.POST.get('product_id'), request)}")


class BoughtProductList(ListView):
    """ Страница с промотром заказов и уже купленных товаров. Войти может только admin """
    template_name = "market/main_market_page.html"
    model = MarketProduct
    login_url = "/login/"

    def get(self, request):
        if request.user.is_superuser:
            return super().get(request)
        else:
            return redirect('/admin/')


class MarketOperations(TemplateView):
    template_name = 'market/market_success.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MarketOperations, self).get_context_data(*args, **kwargs)
        context["message"] = self.request.GET.get('message')
        return context


def _buying_product_from_market(product_id_for_buy: int, request) -> str:
    """
    Производит валидацию данных. Если все данные верны, то происходит покупка.
    Покупка - списание средств и добавление продукта в таблицу с купленными товарами.

    Возвращает 'Success', если средства списали у покупателя и добавился заказ на продукт в таблицу BoughtProduct, иначе
    возвращается сообщение с ошибкой.
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

    bough_product = BoughtProduct(customer=request.user.puples, main_product=product_from_db)
    bough_product.save()

    product_from_db.remained_amount -= 1
    product_from_db.save()

    request.user.puples.rate -= product_from_db.price
    request.user.puples.save()

    return "Success"
