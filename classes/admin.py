import pandas as pd
from django.contrib import admin
from django.http import HttpResponse

from student_database.settings import BASE_DIR
from .models import Classes
from .forms import ClassesForm
from revenue.models import Revenue


class RevenueInline(admin.StackedInline):
    model = Revenue


class MembershipInline(admin.TabularInline):
    model = Classes.students.through


class ClassesAdmin(admin.ModelAdmin):
    list_display = ("groups_details", "instructors", "education", "count_students", "money", "level")
    filter_horizontal = ["students"]
    inlines = [RevenueInline]
    form = ClassesForm
    actions = ["download_excel"]

    def download_excel(self, request, queryset):
        list_class = []
        for i in queryset:
            list_class.append(' ')
            list_class.append("Группа: " + i.name)
            for s in i.students.all():
                list_class.append(s.name)
        result = pd.DataFrame({list_class[0]: list_class[1:]})
        result.to_excel(BASE_DIR / "class.xlsx")
        with open(BASE_DIR / "class.xlsx", "rb") as f:
            response = HttpResponse(f.read())
        response['Content-Type'] = 'text/plain,charset=utf8'
        response['Content-Disposition'] = "attachment; filename=class.xlsx"
        return response







admin.site.register(Classes, ClassesAdmin)
