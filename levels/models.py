from django.db import models


class Levels(models.Model):
    name = models.CharField(max_length=100, verbose_name='Уровень')

    def __str__(self):
        return self.name
