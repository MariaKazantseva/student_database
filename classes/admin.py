from django.contrib import admin
from .models import Classes
from .forms import ClassesForm
from revenue.models import Revenue


class RevenueInline(admin.StackedInline):
    model = Revenue


class MembershipInline(admin.TabularInline):
    model = Classes.students.through


class ClassesAdmin(admin.ModelAdmin):
    list_display = ("groups_details", "instructors", "education", "count_students", "money")
    filter_horizontal = ["students"]
    inlines = [RevenueInline]
    form = ClassesForm


admin.site.register(Classes, ClassesAdmin)
