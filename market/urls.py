from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from . import views

urlpatterns = [
    path('', views.MainMarketPage.as_view(), name='Каталог магазина'),
    path('bought_product_list/', views.BoughtProductList.as_view(), name='Каталог купленных товаров'),
    path('market_success/', views.MarketOperations.as_view(), name="Сообщение после покупки"),
]
