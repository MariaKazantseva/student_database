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
        'money_per_lev': revenue_per_level(date.today()),
        'money_per_age': rev_per_age(date.today()),
        'title': 'Revenue analytics',
        'highlighted': 'revenue',
    }
    return TemplateResponse(request, "analytics_revenue.html", params)


def revenue_per_level(current_date):
    rev_per_lev = Revenue.objects.filter(
        paid_for__month=current_date.month, paid_for__year=current_date.year).values(
        'classes__level__name').annotate(mysum=Sum('amount')).order_by('-mysum')
    result = {'labels': [], 'series': []}
    a = 0
    for i in rev_per_lev:
        a += i['mysum']
    for i in rev_per_lev:
        result['series'].append(round(i['mysum'] * 100 / a))
        result['labels'].append(i['classes__level__name'])
    return result


def rev_per_age(current_date):
    money_per_age = Revenue.objects.filter(paid_for__year=current_date.year).values(
        'student__name', 'student__age').annotate(
        mysum=Sum('amount')).order_by()
    result = {'school_students': 0, 'ЕГЭ': 0, 'adult_students': 0}
    for i in money_per_age:
        age = get_age(i['student__age'], current_date)
        if age < 16:
            result['school_students'] += i['mysum']
        elif age > 18:
            result['adult_students'] += i['mysum']
        else:
            result['ЕГЭ'] += i['mysum']
    final_result = {'labels': [], 'series': []}
    for i in result.keys():
        final_result['series'].append(result[i])
        final_result['labels'].append(i)
    print(final_result)
    return final_result


def get_age(birthday, current_date):
    res = current_date.year - birthday.year
    check_birthday = (current_date.month, current_date.day) < (birthday.month, birthday.day)
    if check_birthday:
        res -= 1
    return res



