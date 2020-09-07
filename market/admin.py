from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import MarketProduct, BoughtProduct


class MarketProductAdmin(admin.ModelAdmin):
    list_display = ("show_image", "product_name", "product_size", "product_color", "price", "remained_amount")
    search_fields = ("product_name", )

    def show_image(self, obj):
        if obj.product_photo:
            return mark_safe(f"<img src='{obj.product_photo.url}' width=75 />")
        return "None"

    show_image.__name__ = "Фото"


class BoughtProductAdmin(admin.ModelAdmin):
    list_display = ("main_product", "customer", "bought_date", "given")
    search_fields = ("main_product", "customer")
    list_filter = ("given", )


admin.site.register(MarketProduct, MarketProductAdmin)
admin.site.register(BoughtProduct, BoughtProductAdmin)
