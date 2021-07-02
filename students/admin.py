from django.contrib import admin
from .models import Students
from .models import Contacts
from revenue.models import Revenue
from classes.admin import MembershipInline


class RevenueInline(admin.TabularInline):
    model = Revenue


class StudentsAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "grade", "count_money"]
    search_fields = ["name", "country"]
    list_filter = ["grade"]
    inlines = [RevenueInline, MembershipInline]


class ContactsAdmin(admin.ModelAdmin):
    list_display = ["email", "whatsapp", "social_media"]


admin.site.register(Students, StudentsAdmin)
admin.site.register(Contacts, ContactsAdmin)
