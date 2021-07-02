from django.contrib import admin
from .models import Revenue


class RevenueAdmin(admin.ModelAdmin):
    list_display = ["date", "paid_for", "student", "classes", "amount", "debtor"]



admin.site.register(Revenue, RevenueAdmin)

