from django.db import models
from django.contrib import admin
from languages.models import Languages
from students.models import Students
from instructors.models import Instructors


class Classes(models.Model):
    your_class_type = [("g", "group"), ("i", "individual")]
    name = models.CharField(max_length=20, verbose_name="Номер группы", null=True, default="Частный урок")
    type = models.CharField(max_length=1, choices=your_class_type, verbose_name="Тип уроков")
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, verbose_name="Язык", null=True)
    students = models.ManyToManyField(Students, verbose_name="Студенты")
    instructors = models.ForeignKey(Instructors, on_delete=models.CASCADE, null=True, verbose_name="Преподаватель")

    @admin.display(description="Образование")
    def education(self):
        return self.instructors.education

    @admin.display(description="Количество студентов", ordering="-count_students")
    def count_students(self):
        return self.students.count()

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = "Class"
        verbose_name_plural = "Classes"
