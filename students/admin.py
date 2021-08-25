from django.contrib import admin
from django.http import HttpResponse

from student_database.settings import BASE_DIR
from .models import Students
from revenue.models import Revenue
from classes.admin import MembershipInline
import pandas as pd


class RevenueInline(admin.TabularInline):
    model = Revenue


class StudentsAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "grade", "count_money", "interest"]
    search_fields = ["name", "country"]
    list_filter = ["grade", "interest"]
    inlines = [RevenueInline, MembershipInline]
    actions = ["download_excel"]

    def download_excel(self, request, queryset):
        list_name, list_interest, list_info = [], [], []
        for i in queryset:
            list_name.append(i.name)
            list_interest.append(i.interest)
            list_info.append(i.additional_info)
        result = pd.DataFrame({"name": list_name, "interested in": list_interest, "info": list_info})
        result.to_excel(BASE_DIR / "students.xlsx")
        # Starting from here we write in details everything about Http responses (like in views!),
        # but we do it manually. Response Headers (I can find info there about Content-Type and Content_Disposition)
        fp = open(BASE_DIR / "students.xlsx", "rb")
        response = HttpResponse(fp.read())
        fp.close()
        file_type = 'text/plain,charset=utf8'
        response['Content-Type'] = file_type
        response['Content-Disposition'] = "attachment; filename=students.xlsx"
        return response

    download_excel.short_description = "Download Excel file for selected stats."


admin.site.register(Students, StudentsAdmin)
