# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

#students

def students_list(request):
    students = (
        {'id': 1,
        'first_name': u'Генрі',
        'last_name': u'Кавілл',
        'ticket': 001,
        'image': 'img/1.jpg'},
        {'id': 2,
        'first_name': u'Джейк',
        'last_name': u'Джилленхол',
        'ticket': 002,
        'image': 'img/2.jpg'},
        {'id': 3,
        'first_name': u'Майкл',
        'last_name': u'Фассбендер',
        'ticket': 003,
        'image': 'img/3.jpg'},
    )
    return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

