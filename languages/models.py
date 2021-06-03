from django.contrib import admin
from django.db import models


class Languages(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Наименование')
    active = models.BooleanField(default=True, verbose_name='Активность')

    @admin.display(description="Количество групп")
    def group_number(self):
        return Languages.objects.filter(groups__language=self).count()

    @admin.display(description="Активность", boolean=True)
    def active_language(self):
        return True if Languages.objects.filter(groups__language=self).count() else False

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Languages"
        verbose_name = "Language"
        ordering = ["name"]
