# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Student, Group

from django.views.generic import UpdateView, DeleteView, CreateView

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
    template_name = 'students/add_edit.html'
    form_class = StudentUpdateForm
    
    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['title'] = u'Редагування студента'
        return context
    
    def get_success_url(self):
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.add_message(request, messages.SUCCESS, "Редагування студента відмінено!")
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.add_message(request, messages.SUCCESS, "Студента успішно збережено!")
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentAddForm(ModelForm):
    class Meta:
        model = Student
        exclude = ()
    
    def __init__(self, *args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper(self)
        
        # set form tag attributes
        self.helper.form_action = reverse('students_add')

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = False
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
    
class StudentAddView(CreateView):
    model = Student
    template_name = 'students/add_edit.html'
    form_class = StudentAddForm

    def get_context_data(self, **kwargs):
        context = super(StudentAddView, self).get_context_data(**kwargs)
        context['title'] = u'Додавання студента'
        return context

    def get_success_url(self):
        return reverse('home')
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.add_message(request, messages.SUCCESS, "Додавання студента скасовано!")
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.add_message(request, messages.SUCCESS, "Студента успішно додано!")
            return super(StudentAddView, self).post(request, *args, **kwargs)
    
    
