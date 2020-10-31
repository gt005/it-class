from django.contrib import admin
from .models import EducationLevel, EducationTask, CheckedEducationTask


admin.site.register(EducationLevel)
admin.site.register(EducationTask)
admin.site.register(CheckedEducationTask)
