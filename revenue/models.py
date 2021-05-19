from django.db import models
from datetime import date, datetime
from students.models import Students
from classes.models import Classes


class Revenue(models.Model):
    date = models.DateField(default=date.today, verbose_name="Дата операции")
    student = models.ForeignKey(Students, verbose_name="Студент", on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, verbose_name="Группа", on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name="Сумма")

    def __str__(self):
        return datetime.strftime(self.date, "%d.%m.%Y")

    class Meta:
        ordering = ["date"]