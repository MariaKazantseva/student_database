from django.shortcuts import render
from collections import Counter
from django.db.models import Sum, Count
from operator import itemgetter
from datetime import date, datetime, timedelta
from django.db.models.functions import TruncMonth, TruncYear, Trunc
from django.template.response import TemplateResponse
from revenue.models import Revenue


def dashboard(request):
    params = {
        'chart_revenue': get_chart_revenue(date.today().year, date.today()),
        'chart_revenue_per_year': revenue_per_year(),
        'students_per_months': students_per_month(date.today()),
        'rev_per_month': rev_per_month(date.today()),
        'percentage_of_students': group_type_percent(date.today()),
        'revenue_per_teacher': revenue_per_teacher(date.today()),
        'revenue_per_lang': revenue_per_lang(date.today()),
        'vip_students': vip_students(date.today()),
        'perc_students_lang': perc_stud_lang(date.today()),
        'money_per_age': rev_per_age(date.today()),
        'money_per_lev': revenue_per_level(date.today()),
    }
    return TemplateResponse(request, "dashboard.html", params)


def get_chart_revenue(year, current_date):
    payments = Revenue.objects.filter(paid_for__year=year).annotate(month=TruncMonth('date')).values('month').annotate(
        mysum=Sum('amount')).order_by('month')
    chart_revenue = {'labels': [], 'series': []}
    for i in payments:
        chart_revenue['labels'].append(i['month'].strftime('%B'))
        chart_revenue['series'].append(i['mysum'])
    return {
        'first': chart_revenue,
        'second': chart_revenue['series'][-1],
        'comparison': comparison_rev(chart_revenue)
    }


def comparison_rev(money_received):
    percentage_money_difference = round(money_received['series'][-1]*100/money_received['series'][-2])
    return {
        'percentage': abs(percentage_money_difference),
        'color': 'text-danger' if percentage_money_difference < 100 else 'text-success',
        'arrow': 'fa-angle-down' if percentage_money_difference < 100 else 'fa-angle-up'
    }


def revenue_per_year():
    money = Revenue.objects.annotate(year=TruncYear('date')).values('year').annotate(
        mysum=Sum('amount')).order_by('year')
    chart_revenue_per_year = {'labels': [], 'series': []}
    for i in money:
        chart_revenue_per_year['labels'].append(i['year'].strftime('%Y'))
        chart_revenue_per_year['series'].append(i['mysum'])
    return chart_revenue_per_year


def students_per_month(current_date):
    students_count = lets_count_students(current_date)
    return {
        'students_count': students_count,
        'start_date': date.strftime(current_date, '%b 1'),
        'end_date': date.strftime(current_date, '%b ' + str(count_days(current_date))),
        'comparison': comparison_perc(current_date, students_count),
    }


def lets_count_students(current_date):
    return Revenue.objects.filter(
        paid_for__month=current_date.month, paid_for__year=current_date.year).values(
        'student').distinct().order_by().count()


def count_days(current_date):
    if current_date.month == 12:
        return 31
    else:
        a = date(current_date.year, current_date.month + 1, 1) - timedelta(days=1)
        return a.day


def comparison_perc(current_date, current_students):
    percentage_current_students = round(100 - current_students*100/lets_count_students(previous_month(current_date)))
    return {
        'percentage': abs(percentage_current_students),
        'color': 'text-danger' if percentage_current_students < 0 else 'text-success',
        'arrow': 'fa-angle-down' if percentage_current_students < 0 else 'fa-angle-down'
    }


def previous_month(current_date):
    if current_date.month == 1:
        return date(current_date.year - 1, 12, 1)
    else:
        return date(current_date.year, current_date.month - 1, 1)


def rev_per_month(current_date):
    rev_per_mon = Revenue.objects.filter(
        paid_for__month=current_date.month, paid_for__year=current_date.year, debtor=False).annotate(month=TruncMonth(
        'paid_for')).values('month').annotate(
        mysum=Sum('amount')).order_by()
    return rev_per_mon


def group_type_percent(current_date):
    percent_of_students = Revenue.objects.filter(
        paid_for__month=current_date.month, paid_for__year=current_date.year).values('student__name',
                                                                                     'classes__type').distinct().order_by()
    count_i = 0
    count_g = 0
    for i in percent_of_students:
        if i['classes__type'] == 'i':
            count_i += 1
        else:
            count_g += 1
    return {
        'i': round(100 * count_i / (count_g + count_i), 1),
        'g': round(100 * count_g / (count_g + count_i), 1),
    }


def revenue_per_teacher(current_date):
    return Revenue.objects.filter(
        paid_for__month=current_date.month, paid_for__year=current_date.year).values(
        'classes__instructors__name').annotate(mysum=Sum('amount')).order_by('-mysum')


def revenue_per_lang(current_date):
    rev_per_lang = Revenue.objects.filter(paid_for__month=current_date.month,
                                          paid_for__year=current_date.year).values(
        'classes__language__name').annotate(mysum=Sum('amount')).order_by('-mysum')
    sum_lang = 0
    for i in rev_per_lang:
        sum_lang += i['mysum']
    result = {'labels': [], 'series': []}
    for i in rev_per_lang:
        result['series'].append(round(i['mysum'] * 100 / sum_lang))
        result['labels'].append(i['classes__language__name'])
    print(result)
    return result


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
    return set(result)


def perc_stud_lang(current_date):
    students_per_languages = Revenue.objects.filter(
        paid_for__month=current_date.month, paid_for__year=current_date.year).values(
        'classes__language__name', 'student__name').distinct().order_by()
    #print(students_per_languages)
    result = []
    for i in students_per_languages:
        result.append(i['classes__language__name'])
    students_per_languages_chart = {'labels': [], 'series': []}
    #print(Counter(result))
    for i in Counter(result).values():
        students_per_languages_chart['series'].append(round(100 * i / students_per_languages.count()))
    for i in Counter(result).keys():
        students_per_languages_chart['labels'].append(i)
    return students_per_languages_chart


def rev_per_age(current_date):
    money_per_age = Revenue.objects.filter(paid_for__year=current_date.year).values('student__name', 'student__age').annotate(
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
    #print(result)
    return result


def get_age(birthday, current_date):
    res = current_date.year - birthday.year
    check_birthday = (current_date.month, current_date.day) < (birthday.month, birthday.day)
    if check_birthday:
        res -= 1
    return res


def vip_per_time(current_date):
    start_date = date(current_date.year - 2, current_date.month, current_date.day)
    end_date = current_date
    vip_people_time = Revenue.objects.filter(paid_for__range=(start_date, end_date)).values('student')


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
    print(result)
    return result





