from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from . import views

urlpatterns = [
    path('', views.MainMarketPage.as_view(), name='Каталог магазина'),
    path('bought_product_list/', views.BoughtProductList.as_view(), name='Каталог купленных товаров'),
    path('market_success/', views.MarketOperations.as_view(), name="Сообщение после покупки"),
    path('shopping_cart/', views.ShoppingCartView.as_view(), name="Корзина с товарами"),
    path('shopping-cart_operations/', views.ShoppingCartOperations.as_view(), name="Работа с корзиной в json")
]
