from django.contrib import admin
from .models import Instructors


class InstructorsAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "group_number", "student_number"]
    search_fields = ["name", "country"]
    list_filter = ["country"]


admin.site.register(Instructors, InstructorsAdmin)
