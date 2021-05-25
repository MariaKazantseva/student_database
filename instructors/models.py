from django.contrib import admin
from django.db import models
from languages.models import Languages
from levels.models import Levels


class Instructors(models.Model):
    name = models.CharField(max_length=100, verbose_name="ФИО")
    experience = models.PositiveSmallIntegerField(default=0, verbose_name="Опыт работы")
    country = models.CharField(max_length=100, default="Russia", verbose_name="Страна")
    specialization = models.CharField(max_length=100, verbose_name="Специализация")
    languages = models.ManyToManyField(Languages)
    levels = models.ManyToManyField(Levels)
    education = models.CharField(max_length=100, verbose_name="Образование")
    activity = models.BooleanField(default=True, verbose_name="Активность")

    @admin.display(description="Количество групп")
    def group_number(self):
        from classes.models import Classes
        return Classes.objects.filter(instructors=self).count()

    @admin.display(description="Количество студентов")
    def student_number(self):
        from classes.models import Classes
        return Classes.objects.filter(instructors=self).values("students")

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"
        ordering = ["name"]
