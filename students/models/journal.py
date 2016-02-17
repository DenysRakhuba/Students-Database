from __future__ import unicode_literals

from django.db import models

class Visit(models.Model):
    
    student = models.ForeignKey('Student',
        max_length=256,
        blank=False,
        verbose_name=u"Студент")