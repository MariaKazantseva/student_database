from django.contrib import admin
from .models import Languages


class LanguagesAdmin(admin.ModelAdmin):
    list_display = ["name", "active", "group_number", "active_language"]
    list_filter = ["active"]
    search_fields = ["name"]
    list_editable = ["active"]


admin.site.register(Languages, LanguagesAdmin)
