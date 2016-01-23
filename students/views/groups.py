# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse


def groups_list(request):
    groups = (
        {'id': 1,
         'title': u'Б1УМБ2',
         'cap': u'Кавілл Генрі'},
        {'id': 2,
         'title': u'Б1УМБ1',
         'cap': u'Джейк Джилленхол'},
        {'id': 3,
         'title': u'Б1УМБ3',
         'cap': u'Фассбендер Майкл'},
    )
    return render(request, 'students/groups.html', {'groups': groups})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)

