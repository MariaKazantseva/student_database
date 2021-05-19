from django.db import models
from phone_field import PhoneField


class Students(models.Model):
    your_gender = [('m', 'male'), ('f', 'female'), ('n', 'not specified')]
    name = models.CharField(max_length=200, verbose_name="ФИО")
    country = models.CharField(max_length=100, default="Russia", verbose_name="Страна")
    gender = models.CharField(max_length=1, choices=your_gender)
    age = models.DateField()
    education = models.CharField(max_length=100, verbose_name="Образование")
    profession = models.CharField(max_length=100, verbose_name="Профессия")
    grade = models.IntegerField(default=0, verbose_name="Класс в школе")

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Contacts(models.Model):
    email = models.EmailField(max_length=254, verbose_name="e-mail address")
    whatsapp = PhoneField()
    social_media = models.URLField(verbose_name="social media links")

    def __str__(self):
        return self.email, self.whatsapp

    class Meta():
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
