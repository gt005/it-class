from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import MarketProduct, BoughtProduct


class MarketProductAdmin(admin.ModelAdmin):
    list_display = ("show_image", "product_name", "product_size", "product_color", "price", "remained_amount", "visibility_to_customers")
    search_fields = ("product_name", )
    list_filter = ("visibility_to_customers",)
    actions = ["show_all_products_to_users", "hide_products_from_users"]

    def show_image(self, obj):
        if obj.product_photo:
            return mark_safe(f"<img src='{obj.product_photo.url}' width=75 />")
        return "None"

    def show_all_products_to_users(self, request, queryset):
        row_update = queryset.update(visibility_to_customers=True)
        self.message_user(request, f"Записей обновлено: {row_update}")

    def hide_products_from_users(self, request, queryset):
        row_update = queryset.update(visibility_to_customers=False)
        self.message_user(request, f"Записей обновлено: {row_update}")

    show_all_products_to_users.short_description = "Сделать видимыми для покупателей"
    show_all_products_to_users.allowed_permissions = ("change",)

    hide_products_from_users.short_description = "Сделать невидимыми для покупателей"
    hide_products_from_users.allowed_permissions = ("change",)

    show_image.__name__ = "Фото"


class BoughtProductAdmin(admin.ModelAdmin):
    list_display = ("main_product", "customer", "bought_date", "given")
    search_fields = ("main_product", "customer")
    list_filter = ("given", )


admin.site.register(MarketProduct, MarketProductAdmin)
admin.site.register(BoughtProduct, BoughtProductAdmin)
