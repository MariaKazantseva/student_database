from django.contrib import admin
from .models import Classes
from revenue.models import Revenue


class RevenueInline(admin.StackedInline):
    model = Revenue


class MembershipInline(admin.TabularInline):
    model = Classes.students.through


class ClassesAdmin(admin.ModelAdmin):
    list_display = ("name", "instructors", "education", "count_students")
    filter_horizontal = ["students"]
    inlines = [RevenueInline]


admin.site.register(Classes, ClassesAdmin)
