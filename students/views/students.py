# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime

from ..models import Student, Group

from django.views.generic import UpdateView, DeleteView

from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from django.contrib import messages

#students

def students_list(request):
    students = Student.objects.all()
    
    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    
# paginate students
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        students = paginator.page(paginator.num_pages)        
    
    return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
    #checkin' if form was posted
    if request.method == "POST":
        #checkin' if was a button clicked
        if request.POST.get('add_button') is not None:
            #TODO: validate input from user
            errors = {}
            #validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}
            #validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name
                
            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name
            
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday
                
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket
            
            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                messages.error(request, "Оберіть групу для студента")
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    messages.add_message(request, message.error, "Оберіть коректну групу")
                else:
                    data['student_group'] = groups[0]
                
            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo
                
            #save student
            if not errors:
                #create new student
                student = Student(**data)
                student.save()
                
                messages.add_message(request, messages.SUCCESS, "Студента на iм'я {} {} успішно додано!".format(student.first_name, student.last_name))
                return HttpResponseRedirect(reverse('home'))
            
            else:
                #render from with errors and previous user input
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})
                              
        elif request.POST.get('cancel_button') is not None:
            #redirect to home page
            messages.add_message(request, messages.SUCCESS, "Додавання студента скасовано!")
            return HttpResponseRedirect(reverse('home'))
    else:
        #initial form render
        return render(request, 'students/students_add.html',
                      {'groups': Group.objects.all().order_by('title')})



class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'
    
    def get_success_url(self):
        return u'%s?status_message=Студента успішно видалено!' % reverse('home')

class StundentUpdateForm(forms.Form):
    first_name = forms.CharField(
        label="Ім'я*"
    )
    last_name = forms.CharField(
        label="Прізвище*"
    )
    middle_name = forms.CharField(
        label="По-батькові"
    )
    birthday = forms.DateField(
        label="Дата народждення*",
        input_formats="%m/%d/%Y"
    )
    photo = forms.ImageField(
        label="Фото"
    )
    ticket = forms.CharField(
        label="Білет*"
    )
    notes = forms.CharField(
        label="Додаткові нотатки"
    )
                
        
def students_edit(request):
    form = StudentUpdateForm(request.POST)
    
    if form.is_valid():
        return HttpResponseRedirect('home')
    
    else:
        form = StudentUpdateForm()
    return render(request, 'students/students_edit.html', {'form': form})
    

        
        