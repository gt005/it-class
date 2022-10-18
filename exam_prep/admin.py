from django.contrib import admin
from .models import Task, Variant
import json

class TaskAdmin(admin.ModelAdmin):
    list_display = ("id_task", "number_ege", "result")
    list_display_links = ("id_task",)
    list_filter = ("number_ege",)
    search_fields = ("id_task",)

class VariantAdmin(admin.ModelAdmin):
    list_display = ("id_var", "name_puple", "list_tasks")
    list_display_links = ("id_var",)

    def name_puple(self, obj):
        return obj.puples

    def list_tasks(self, obj):
        tdict = {}
        tmp  = json.loads(obj.tasks)
        for i in tmp:
            tdict[i] = Task.objects.get(number_ege=i, number_task=int(tmp[i])).id_task
        return list(tdict.items())


admin.site.register(Task, TaskAdmin)
admin.site.register(Variant, VariantAdmin)
