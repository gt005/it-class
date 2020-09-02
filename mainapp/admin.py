from django.contrib import admin

from .models import Puples, Events, Works, DaysTask, ApplicantAction, SummerPractice
from market.models import MarketProduct, BoughtProduct


class EventsAdmin(admin.ModelAdmin):
    list_display = ("date", "name", "events")
    list_display_links = ("name",)
    list_filter = ("date", "name", "events__surname")
    search_fields = ("name", "events__surname", "events__name")


class WorksAdmin(admin.ModelAdmin):
    list_display = ("date", "name")
    list_filter = ("date", "name")
    list_display_links = ("name",)


class ApplicantActionAdmin(admin.ModelAdmin):
    list_display = ("action_app", "check", "date")
    search_fields = ("action_app__name", "action_app__surname")
    list_filter = ("action_app__surname", "date")


class PuplesAdmin(admin.ModelAdmin):
    list_display = ("surname", "name", "status")
    list_filter = ("surname", "status")
    actions = ["change_class_10", "change_class_11"]

    def change_class_10(self, request, queryset):
        row_update = queryset.update(status="ST10")
        if row_update == 1:
            message_bit = "1 запись обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def change_class_11(self, request, queryset):
        row_update = queryset.update(status="ST11")
        if row_update == 1:
            message_bit = "1 запись обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    change_class_11.short_description = "Перевести ученика в 11 класс"
    change_class_11.allowed_permissions = ("change",)

    change_class_10.short_description = "Перевести ученика в 10 класс"
    change_class_10.allowed_permissions = ("change",)


class MarketProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "product_size", "product_color", "price", "remained_amount")
    search_fields = ("product_name", )


class BoughtProductAdmin(admin.ModelAdmin):
    list_display = ("main_product", "customer", "bought_date", "given")
    search_fields = ("main_product", "customer")
    list_filter = ("given", )


admin.site.register(Puples, PuplesAdmin)
admin.site.register(SummerPractice)
admin.site.register(Events, EventsAdmin)
admin.site.register(Works, WorksAdmin)
admin.site.register(DaysTask)
admin.site.register(ApplicantAction, ApplicantActionAdmin)
admin.site.register(MarketProduct, MarketProductAdmin)
admin.site.register(BoughtProduct, BoughtProductAdmin)
