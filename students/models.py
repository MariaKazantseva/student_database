from django.contrib import admin
from django.db import models
from django.db.models import Sum
from phone_field import PhoneField


class Students(models.Model):
    your_gender = [('m', 'male'), ('f', 'female'), ('n', 'not specified')]
    name = models.CharField(max_length=200, verbose_name="ФИО")
    country = models.CharField(max_length=100, default="Russia", verbose_name="Страна")
    gender = models.CharField(max_length=1, choices=your_gender)
    age = models.DateField()
    education = models.CharField(max_length=100, verbose_name="Образование")
    additional_info = models.TextField(max_length=10000, verbose_name="Дополнительная информация", null=True, blank=True)
    grade = models.IntegerField(default=0, verbose_name="Класс в школе")
    email = models.EmailField(max_length=254, verbose_name="e-mail address", blank=True)
    whatsapp = PhoneField(blank=True)
    social_media = models.URLField(verbose_name="social media links", blank=True)

    @admin.display(description="Сумма")
    def count_money(self):
        return Students.objects.filter(people__student=self).aggregate(mySum=Sum('people__amount'))['mySum'] or 0.0

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = "Student"
        verbose_name_plural = "Students"



