import json
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from mainapp.addons_python.views_addons_functions import *
from mainapp.addons_python.views_addons_classes import HeaderNotificationsCounter

from .market_services.market_operations import *
from .market_services.market_classes import ShoppingCart
from .models import MarketProduct, BoughtProduct


class MainMarketPage(HeaderNotificationsCounter, LoginRequiredMixin, ListView):
    """ Страница с каталогом товаров магазина """
    template_name = "market/main_market_page.html"
    model = MarketProduct
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        recount_all_peoples_rating()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainMarketPage, self).get_context_data(**kwargs)
        context['shopping_cart_list'] = ShoppingCart(self.request).get_shopping_cart_list()
        return context


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


class ShoppingCartView(HeaderNotificationsCounter, TemplateView):
    template_name = "market/shopping_cart.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ShoppingCartView, self).get_context_data(**kwargs)
        context["shopping_cart_items"] = ShoppingCart(request=self.request)
        return context


class ShoppingCartOperations(LoginRequiredMixin, View):
    def get(self, request):
        cart = ShoppingCart(request)

        if "add_product" in request.GET:
            msg = cart.add(request.GET["add_product"])
        elif "remove_product" in request.GET:
            msg = cart.remove(request.GET["remove_product"])

        return JsonResponse({'message': msg})