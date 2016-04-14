# -*- coding: utf-8 -*-
from django import forms
from django.views.generic.edit import FormView

from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from studentsdb.settings import ADMIN_EMAIL

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, label=u"Ваше Ім'я")
    contact_email = forms.EmailField(required=True, label=u"Ваша Емейл Адреса")
    text = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label=u"Текст повідомлення"
    )
    
    def __init__(self, *args, **kwargs):
    # call original initializator
        super(ContactForm, self).__init__(*args, **kwargs)
        
        # this helper object allows us to customize form
        self.helper = FormHelper()
       
        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'

        
        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        
        # form buttons
        self.helper.add_input(Submit('send_button', u'Надіслати'))
    
class ContactAdmin(FormView):
    template_name = 'contact_admin/contact.html'
    form_class = ContactForm
    
    
    def get_success_url(self):
        return u'%s?status_message=Повідомлення успішно надіслано.' % reverse('contact')  

    def form_valid(self, form):
        text = form.cleaned_data['text']
        contact_name = form.cleaned_data['contact_name']
        contact_email = form.cleaned_data['contact_email']
        
        try:
            text += (u'\n E-mail відправлено від - %s, %s') % (contact_name, contact_email)
            send_mail(contact_name, text, contact_email, [ADMIN_EMAIL])
        
        except Exception:
            return HttpResponseRedirect(
                u'%s?status_message=Під час відправки листа виникла непередбачувана помилка.' %
                reverse('contact'))            
 
            
        return super(ContactAdmin, self).form_valid(form)
    
