from django.contrib import admin
from .models import Levels


class LevelsAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Levels, LevelsAdmin)