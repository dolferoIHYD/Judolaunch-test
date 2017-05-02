# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Task
from .forms import AddTaskForm


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks':tasks})


def add_task(request):
    if request.method == 'GET':
        pass
