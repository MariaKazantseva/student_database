from django.db.models import Sum
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib import admin
from languages.models import Languages
from students.models import Students
from instructors.models import Instructors
from levels.models import Levels


class Classes(models.Model):
    your_class_type = [("g", "group"), ("i", "individual")]
    name = models.CharField(max_length=20, verbose_name="Номер группы", null=True, default="Частный урок")
    type = models.CharField(max_length=1, choices=your_class_type, verbose_name="Тип уроков")
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, verbose_name="Язык", null=True,
                                 related_name="groups")
    students = models.ManyToManyField(Students, verbose_name="Студенты")
    instructors = models.ForeignKey(Instructors, on_delete=models.CASCADE, null=True, verbose_name="Преподаватель")
    start_date = models.DateField(verbose_name="Дата начала", null=True, blank=True)
    end_date = models.DateField(verbose_name="Дата окончания", null=True, blank=True)
    level = models.ForeignKey(Levels, verbose_name='Уровень', on_delete=models.CASCADE, null=True)

    @admin.display(description="Образование")
    def education(self):
        return self.instructors.education

    @admin.display(description="Количество студентов", ordering="-count_students")
    def count_students(self):
        return self.students.count()

    @admin.display(description="Сумма")
    def money(self):
        return Classes.objects.filter(groups__classes=self).aggregate(mySum=Sum('groups__amount'))['mySum'] or 0.0

    @admin.display(description="Уроки")
    def groups_details(self):
        return self

    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({
                    'start_date': ValidationError(_('Incorrect date')),
                    'end_date': ValidationError(_('Incorrect date')),
                })
        if not self.start_date and self.end_date:
            raise ValidationError({'start_date': _('Input start date')})


    def __str__(self):
        year = datetime.strftime(self.start_date, "%Y") if self.start_date else "0000"
        temp = f"{year}.{self.type.upper()}."
        if self.type == "g":
            return f"{temp}{self.name}"
        else:
            return f"{temp}{str(self.pk).zfill(4)}"

    class Meta():
        verbose_name = "Class"
        verbose_name_plural = "Classes"
