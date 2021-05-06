from django.db import models


class Languages(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Наименование')
    active = models.BooleanField(default=True, verbose_name='Активность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Languages"
        verbose_name = "Language"
        ordering = ["name"]