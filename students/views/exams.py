# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Exam

from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView, CreateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions

from django.contrib import messages

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

class ExamAddForm(ModelForm):
    class Meta:
        model = Exam
        exclude = ()
    
    def __init__(self, *args, **kwargs):
        super(ExamAddForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper(self)
        
        # set form tag attributes
        self.helper.form_action = reverse('exams_add')

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        
        # add buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        )
    

class ExamAddView(CreateView):
    model = Exam
    template_name = 'students/add_edit.html'
    form_class = ExamAddForm
    
    def get_context_data(self, **kwargs):
        context = super(ExamAddView, self).get_context_data(**kwargs)
        context['title'] = u'Додавання іспиту'
        return context

    def get_success_url(self):
        return reverse('exams')
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.add_message(request, messages.SUCCESS, "Додавання іспиту скасовано!")
            return HttpResponseRedirect(reverse('exams'))
        else:
            messages.add_message(request, messages.SUCCESS, "Іспит успішно додано!")
            return super(ExamAddView, self).post(request, *args, **kwargs)
    




class ExamUpdateForm(ModelForm):
    class Meta:
        model = Exam
        exclude = ()
    
    def __init__(self, *args, **kwargs):
        super(ExamUpdateForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper(self)
        
        # set form tag attributes
        self.helper.form_action = reverse('exams_edit',
            kwargs={'pk': kwargs['instance'].id})

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        
        # add buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        )

class ExamUpdateView(UpdateView):
    model = Exam
    template_name = 'students/add_edit.html'
    form_class = ExamUpdateForm
    
    def get_context_data(self, **kwargs):
        context = super(ExamUpdateView, self).get_context_data(**kwargs)
        context['title'] = u'Редагування іспиту'
        return context
    
    def get_success_url(self):
        return reverse('exams')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.add_message(request, messages.SUCCESS, "Редагування іспиту відмінено!")
            return HttpResponseRedirect(reverse('exams'))
        else:
            messages.add_message(request, messages.SUCCESS, "Іспит успішно збережено!")
            return super(ExamUpdateView, self).post(request, *args, **kwargs)


class ExamDeleteView(DeleteView):
    model = Exam
    template_name = 'students/exams_confirm_delete.html'
    
