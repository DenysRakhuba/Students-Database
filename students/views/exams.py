# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Exam


def exams_list(request):
    exams = Exam.objects.all()
    
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'title', 'date_and_time', 'teacher', 'group'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()
    
    paginator = Paginator(exams, 3)
    page = request.GET.get('page')
    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        exams = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        exams = paginator.page(paginator.num_pages)        
    
    return render(request, 'students/exams.html', {'exams': exams})

def exams_add(request):
    return HttpResponse('<h1>Exam Add Form</h1>')

def exams_edit(request, gid):
    return HttpResponse('<h1>Edit Exam %s</h1>' % gid)

def exams_delete(request, gid):
    return HttpResponse('<h1>Delete Exam %s</h1>' % gid)

