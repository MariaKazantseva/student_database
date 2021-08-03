from django.shortcuts import render
from collections import Counter
from django.db.models import Sum, Count
from operator import itemgetter
from datetime import date, datetime, timedelta
from django.db.models.functions import TruncMonth, TruncYear, Trunc
from django.template.response import TemplateResponse
from revenue.models import Revenue
from django.shortcuts import render


def main(request):
    params = {
        'vip_students': vip_students(date.today()),
        'title': 'Students analytics',
        'highlighted': 'student',
    }
    return TemplateResponse(request, "analytics_students.html", params)


def vip_students(current_date):
    profitable_students = Revenue.objects.filter(
        paid_for__month=current_date.month, paid_for__year=current_date.year).values(
        'student__name', 'classes__pk').distinct()
    vip_people, result = [], []
    for i in profitable_students:
        vip_people.append(i['student__name'])
        for n in vip_people:
            if vip_people.count(n) > 1:
                result.append(n)
    final_result = []
    for i in result:
        if i not in final_result:
            final_result.append(i)
    print(final_result)
    print(request_info(final_result, current_date))
    return request_info(final_result, current_date)


def request_info(students_params, current_date):
    info = Revenue.objects.filter(
        paid_for__month=current_date.month, paid_for__year=current_date.year, student__name__in=students_params).values(
        'student__name', 'student__email').annotate(mesum=Sum('amount')).order_by()
    return info


