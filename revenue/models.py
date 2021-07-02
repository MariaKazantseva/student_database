from django.db import models
from datetime import date, datetime
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from students.models import Students
from classes.models import Classes


class Revenue(models.Model):
    paid_for = models.DateField(default=date.today, verbose_name='Период оплаты', blank=True, null=True)
    date = models.DateField(default=date.today, verbose_name="Дата операции")
    student = models.ForeignKey(Students, verbose_name="Студент", on_delete=models.CASCADE, related_name="people")
    classes = models.ForeignKey(Classes, verbose_name="Группа", on_delete=models.CASCADE, related_name="groups")
    amount = models.FloatField(verbose_name="Сумма")
    debtor = models.BooleanField(verbose_name='Должники', default=False)

    def clean(self):
        if not Classes.objects.filter(students=self.student, pk=self.classes.pk).exists():
            raise ValidationError({'classes': _('Choose another group')})

    def __str__(self):
        return datetime.strftime(self.paid_for, "%d.%m.%Y")

    class Meta:
        ordering = ["date"]