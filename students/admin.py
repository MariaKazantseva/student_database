from django.contrib import admin
from .models import Students
from revenue.models import Revenue
from classes.admin import MembershipInline


class RevenueInline(admin.TabularInline):
    model = Revenue


class StudentsAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "grade", "count_money"]
    search_fields = ["name", "country"]
    list_filter = ["grade"]
    inlines = [RevenueInline, MembershipInline]


admin.site.register(Students, StudentsAdmin)
