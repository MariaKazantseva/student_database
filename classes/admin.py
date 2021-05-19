from django.contrib import admin
from .models import Classes
from revenue.models import Revenue


class RevenueInline(admin.StackedInline):
    model = Revenue


class ClassesAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [RevenueInline]


admin.site.register(Classes, ClassesAdmin)
