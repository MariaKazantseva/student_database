from django.contrib import admin
from .models import Students
from .models import Contacts


class StudentsAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "grade"]
    search_fields = ["name", "country"]
    list_filter = ["age", "grade"]

class ContactsAdmin(admin.ModelAdmin):
    list_display = ["email", "whatsapp", "social_media"]


admin.site.register(Students, StudentsAdmin)
admin.site.register(Contacts, ContactsAdmin)

