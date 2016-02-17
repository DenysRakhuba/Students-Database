# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Exam(models.Model):
    
    class Meta(object):
        verbose_name = u"Іспит"
        verbose_name_plural = u"Іспити"
        ordering = ['title']
           
        
    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Предмет")
             
    
    date_and_time = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Дата та час проведення")
    
    teacher = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Викладач")
    
    group = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Група")
    
    
    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.group)
