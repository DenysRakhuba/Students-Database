# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ContactForm(forms.Form):
    
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
    
    contact_name = forms.CharField(required=True, label=u"Ваше Ім'я")
    contact_email = forms.EmailField(required=True, label=u"Ваша Емейл Адреса")
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label=u"Текст повідомлення"
    )

def contact_admin(request):
    form_class = ContactForm
    
    return render(request, 'contact_admin/contact.html', {
        'form': form_class,
    })
