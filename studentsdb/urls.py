from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from students.views.students import StudentDeleteView, StudentUpdateView, StudentAddView
from students.views.groups import GroupDeleteView, GroupAddView, GroupUpdateView
from students.views.exams import ExamDeleteView, ExamAddView, ExamUpdateView
from students.views.contact_admin import ContactAdmin


urlpatterns = patterns('',
    # Students urls
    url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^students/add/$', StudentAddView.as_view(),
         name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$',
        StudentUpdateView.as_view(),
        name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$',
        StudentDeleteView.as_view(),
        name='students_delete'),

    # Groups urls
    url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
    url(r'^groups/add/$', GroupAddView.as_view(),
         name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(),
         name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(),
         name='groups_delete'),

    #exams
    url(r'^exams/$', 'students.views.exams.exams_list', name='exams'), 
    url(r'^exams/add/$', ExamAddView.as_view(),
         name='exams_add'),
    url(r'^exams/(?P<pk>\d+)/edit/$', ExamUpdateView.as_view(),
         name='exams_edit'),
    url(r'^exams/(?P<pk>\d+)/delete/$', ExamDeleteView.as_view(),
         name='exams_delete'),
    
    #contact
    url(r'^contact/$', ContactAdmin.as_view(), name='contact'),
    
               
    #journal urls
    url(r'^journal/$', 'students.views.journal.journal_list', name='journal'),           


    url(r'^admin/', include(admin.site.urls)),
)

from .settings import MEDIA_ROOT, DEBUG
# serve files from media folder
if DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT}))