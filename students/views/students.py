# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime

from ..models import Student, Group

from django.views.generic import UpdateView, DeleteView

from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
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
                errors['test'] = messages.error(request, u"Ім'я є обов'язковим", extra_tags='first')
                #errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name
                
            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['test'] = messages.error(request, u"Прізвище є обов'язковим", extra_tags='last')
                #errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name
            
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['test'] = messages.error(request, u"Дата народження є обов'язковою", extra_tags='birth')
                #errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['test'] = messages.error(request, u"Введіть коректний формат дати (напр. 1984-12-30)", extra_tags='birth')
                    #errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday
                
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['test'] = messages.error(request, u"Номер білета є обов'язковим", extra_tags='ticket')
                #errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket
            
            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['test'] = messages.error(request, u"Оберіть групу для студента", extra_tags='group')
                #errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['test'] = messages.error(request, u"Оберіть коректну групу", extra_tags='group')
                    #errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]
            
            MAX_SIZE = 2097152

            photo = request.FILES.get('photo')
            if photo:
                file_extensions = ['jpeg','.jpg','.gif']
                name_file = str(photo.name)
                # typed = str(photo.content_type)
                if photo.size > MAX_SIZE:
                    errors['test'] = messages.error(request, u"Розмір фото перевищує 2 МБ", extra_tags='photo')
                    #errors['photo'] = u"Розмір фото перевищує 2 МБ"
                elif name_file[-4:] not in file_extensions:
                    errors['test'] = messages.error(request,u"Данний тип фото не підтримується. Змініть на: *.jpg, *.jpeg, *.gif", extra_tags='photo')
                    #errors['photo'] = u"Данний тип фото не підтримується. Змініть на: *.jpg, *.jpeg, *.gif"
                    # errors['photo'] = str(photo.name)
                else:
                    data['photo'] = photo
                    
            #save student
            if not errors:
                #create new student
                student = Student(**data)
                student.save()
                
                messages.add_message(request, messages.SUCCESS, "Студента на iм'я {} {} успішно додано!".format(student.first_name, student.last_name), extra_tags='ok')
                return HttpResponseRedirect(reverse('home'))
            
            else:
                #render from with errors and previous user input
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})
                              
        elif request.POST.get('cancel_button') is not None:
            #redirect to home page
            messages.add_message(request, messages.SUCCESS, "Додавання студента скасовано!", extra_tags='cancel')
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

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        exclude = ()
        
    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper(self)
        
        # set form tag attributes
        self.helper.form_action = reverse('students_edit',
            kwargs={'pk': kwargs['instance'].id})

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        
        # add buttons
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'middle_name',
            'birthday',
            'photo',
            'ticket',
            'student_group',
            'notes',
            Submit('add_button', u'Зберегти', css_class="btn btn-primary col-sm-offset-3"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
            )
        
class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm
    
    def get_success_url(self):
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.add_message(request, messages.SUCCESS, "Редагування студента відмінено!")
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.add_message(request, messages.SUCCESS, "Студента успішно збережено!")
            return super(StudentUpdateView, self).post(request, *args, **kwargs)

        
