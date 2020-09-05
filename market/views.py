from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from mainapp.addons_python.views_addons_functions import recount_all_peoples_rating
from mainapp.addons_python.views_addons_classes import HeaderNotificationsCounter

from .market_services.market_operations import *
from .models import MarketProduct, BoughtProduct


class MainMarketPage(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    """ Страница с каталогом товаров магазина """
    template_name = "market/main_market_page.html"
    model = MarketProduct
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        recount_all_peoples_rating()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        buying_result = buying_product_from_market(
            product_id_for_buy=request.POST.get('product_id'),
            request=request)
        return redirect(f"/market/market_success/?message={buying_result}")


class BoughtProductList(HeaderNotificationsCounter, ListView):
    """ Страница с промотром заказов и уже купленных товаров. Войти может только admin """
    template_name = "market/product_check_list.html"
    model = BoughtProduct

    def post(self, request):
        if not request.user.is_superuser:
            return redirect("/admin/")

        if request.POST.get("action-give"):
            give_product_to_customer(
                product_to_give_id=request.POST.get("product_id"),
                request=request
            )
        elif request.POST.get("action-cancel"):
            cancel_given_product_to_customer(
                product_to_cancel_id=request.POST.get("product_id"),
                request=request
            )

        return redirect("/market/bought_product_list/")

    def get_context_data(self, **kwargs):
        context = super(BoughtProductList, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context["not_given_product_list"] = BoughtProduct.objects.filter(given=0)
            context["given_product_list"] = BoughtProduct.objects.filter(given=1)
        else:
            context["not_given_product_list"] = BoughtProduct.objects.filter(given=0, customer=self.request.user.puples)
            context["given_product_list"] = BoughtProduct.objects.filter(given=1, customer=self.request.user.puples)
        return context


class MarketOperations(HeaderNotificationsCounter, TemplateView):
    template_name = "market/market_success.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MarketOperations, self).get_context_data(*args, **kwargs)
        context["message"] = self.request.GET.get("message")
        return context

