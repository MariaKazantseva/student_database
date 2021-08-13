from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from collections import Counter
from django.db.models import Sum, Count
from operator import itemgetter
from datetime import date, datetime, timedelta
from django.db.models.functions import TruncMonth, TruncYear, Trunc
from django.template.response import TemplateResponse
from revenue.models import Revenue
from django.shortcuts import render


@login_required()
def main(request):
    params = {
        'vip_students': vip_students(date.today()),
        'title': 'Students analytics',
        'highlighted': 'student',
        'vip_students_2': vip_students_2(date.today()),
        'percentage_stud_lang': percentage_stud_lang(date.today()),
    }
    return TemplateResponse(request, "analytics_students.html", params)


def vip_students(current_date):
    profitable_students = Revenue.objects.filter(
        paid_for__month=current_date.month, paid_for__year=current_date.year).values(
        'student__name', 'student__email', 'classes__pk').annotate(mysum=Sum('amount')).order_by()
    print(profitable_students)
    temp, result = [], []
    for i in profitable_students:
        if i['student__name'] in temp:
            continue
        count = 0
        tsum = 0
        for n in profitable_students:
            if i['student__name'] == n['student__name']:
                tsum += n['mysum']
                count += 1
            if count > 1:
                i['mysum'] = tsum
                result.append(i)
                temp.append(i['student__name'])
    return result
    print(result)


def vip_students_2(current_date):
    my_students = Revenue.objects.filter(paid_for__year__in=[current_date.year - 1, current_date.year]).filter(
        paid_for__month__in=[1, 2, 3, 4, 5, 9, 10, 11, 12]).values(
        'student__name', 'paid_for__year', 'paid_for__month').distinct().order_by()
    my_result, final_result = [], ''
    for i in my_students:
        my_result.append(i['student__name'])
    for k, v in Counter(my_result).items():
        if v >= 18:
            final_result += k
    return choose_students(final_result, current_date)


def choose_students(important_students, current_date):
    return Revenue.objects.filter(paid_for__year__in=[current_date.year - 1, current_date.year]).filter(
        student__name=important_students).values(
        'student__name', 'student__email').annotate(mysum=Sum('amount')).order_by()


def percentage_stud_lang(current_date):
    students_per_languages = Revenue.objects.filter(
        paid_for__month=current_date.month, paid_for__year=current_date.year).values(
        'classes__language__name', 'student__name').distinct().order_by()
    result = []
    for i in students_per_languages:
        result.append(i['classes__language__name'])
    print(Counter(result).values())
    students_per_languages_chart = {'labels': [], 'series': []}
    for i in Counter(result).values():
        students_per_languages_chart['series'].append(i)
    for i in Counter(result).keys():
        students_per_languages_chart['labels'].append(i)
    print(students_per_languages_chart)
    return students_per_languages_chart
