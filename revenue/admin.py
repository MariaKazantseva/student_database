from django.contrib import admin
from .models import Revenue


class RevenueAdmin(admin.ModelAdmin):
    list_display = ["date", "student", "classes", "amount"]



admin.site.register(Revenue, RevenueAdmin)

