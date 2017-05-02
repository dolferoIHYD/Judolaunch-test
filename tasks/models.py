# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """ docstring for Task """
    name = models.CharField(max_length=50, default='Task name')
    description = models.CharField(max_length=500, default='Task description')
    done = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True)
    done_by = models.ForeignKey(User, related_name='done_set', null=True)

    def __unicode__(self):
        return self.name
