from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from operator import itemgetter
from datetime import date, datetime, timedelta
from django.db.models.functions import TruncMonth, TruncYear, Trunc
from django.template.response import TemplateResponse
from revenue.models import Revenue
from django.shortcuts import render
from instructors.models import Instructors


@login_required()
def main(request):
    best_teacher = revenue_per_teacher(date.today())
    params = {
        'revenue_per_teacher': best_teacher,
        'students_per_teacher': lets_count_students(date.today(), best_teacher['best_teacher']),
        'title': 'Instructors analytics',
        'highlighted': 'instructor',
    }
    return TemplateResponse(request, "analytics_instructors.html", params)


def revenue_per_teacher(current_date):
    money_teachers = Revenue.objects.filter(
        paid_for__month=current_date.month, paid_for__year=current_date.year).values(
        'classes__instructors__name', 'classes__instructors__experience',
        'classes__instructors__country', 'classes__instructors__education',
        'classes__instructors__specialization', 'classes__instructors__languages__name').annotate(
        mysum=Sum('amount')).order_by('-mysum')
    print(money_teachers)
    result = {'labels': [], 'series': []}
    a, b, c, d, e, f = 0, [], [], [], [], []
    for i in money_teachers:
        a += i['mysum']
    for i in money_teachers:
        result['series'].append(round(i['mysum'] * 100 / a))
        result['labels'].append(i['classes__instructors__name'])
        b.append(i['classes__instructors__experience'])
        c.append(i['classes__instructors__country'])
        d.append(i['classes__instructors__education'])
        e.append(i['classes__instructors__specialization'])
        f.append(i['classes__instructors__languages__name'])
    print(result)
    return {
        'chart': result,
        'best_teacher': result['labels'][0],
        'experience': b[0],
        'country': c[0],
        'edu': d[0],
        'spec': e[0],
        'lang': f[0]
    }


def lets_count_students(current_date, best_prof):
    return Revenue.objects.filter(
        paid_for__month=current_date.month, paid_for__year=current_date.year,
        classes__instructors__name=best_prof).values(
        'student').distinct().order_by().count()
