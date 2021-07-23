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
    return TemplateResponse(request, "analytics_students.html", {'title': 'Students analytics', 'highlighted': 'student'})
