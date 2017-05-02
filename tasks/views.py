# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, JsonResponse

from .models import Task
from .forms import AddTaskForm, EditTaskForm


@require_http_methods(['GET', 'POST'])
def login_view(request):
    """
        Do you really need comment here?
    """
    if request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('/')
        else:
            return render(request, 'login.html')
    else:
        data = request.POST
        try:
            user_obj = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Incorrect username'})
        user = authenticate(username=user_obj.username,
                            password=data['password'])
        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Incorrect username \
                                                            or password'})


@require_http_methods(['GET', 'POST'])
def register_view(request):
    """
        Registration. Just like all registrations on Earth.
    """
    if request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('/')
        else:
            return render(request, 'register.html')
    else:
        data = request.POST
        if data['password'] == data['pass_again']:
            user = User.objects.create_user(first_name=data['first_name'],
                                            last_name=data['last_name'],
                                            username=data['username'],
                                            password=data['password'])
        else:
            return render(request, 'register.html', 'Passwords are different')
        login(request, user)
        return redirect('/')


@require_http_methods(['GET'])
def logout_view(request):
    """
        Logouts user
    """
    logout(request)
    return redirect('/')


@login_required()
@require_http_methods(['GET'])
def task_list_view(request):
    """
        Task list. In GET can be param undone.
        If undone, then show only tasks, where done==False.
        I'm a backend dev, so doing it on back.
    """
    filtr = request.GET.get('undone', '')
    if filtr:
        tasks = Task.objects.filter(done='False')
    else:
        tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks':tasks})


@login_required()
@require_http_methods(['GET', 'POST'])
def add_task_view(request):
    """
        Add new task view.

        On GET returns template with creation form, on POST creates task object.
        Returns redirect to task list.
    """
    if request.method == 'GET':
        form = AddTaskForm()
        return render(request, 'add_task.html', {'form': form})
    else:
        form = AddTaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            task = Task.objects.create(name = data['name'],
                                       description = data['description'],
                                       created_by = request.user)
            return redirect('/')
        else:
            return render(request, 'add_task.html', {'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def edit_task_view(request, task_id):
    """
        Take, on get - return it, on POST - rewrite object and save.
        Boring!
    """
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404()
    if request.method == 'GET':
        form = EditTaskForm(instance=task)
        return render(request, 'edit_task.html', {'form': form})
    else:
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            data = form.save()
        else:
            return render(request, 'edit_task.html', {'form': form})
        return redirect('/')


@csrf_exempt
@require_http_methods(['POST'])
def mark_tasks_as_done_view(request):
    """
        View marks tasks as done.

        Front POST data on click to checkbox.
        Check, if task with this id isn't done, ONLY THEN switch them to
        done (because you cant undone your task=) ).
        Responses are not reading in frontend.
    """
    task_id = int(request.POST['task_id'])
    try:
        task = Task.objects.get(id = task_id)
    except Task.DoesNotExist:
        return JsonResponse({'ok': 'not ok'})
    if not task.done:
        task.done = True
        task.done_by = request.user
        task.save()
    return JsonResponse({'ok': 'ok'})


@login_required
@require_http_methods(['GET'])
def delete_task_view(request, task_id):
    """
        Just get task object and delete it. Nothing magical.
    """
    try:
        task = Task.objects.get(id = task_id)
    except Task.DoesNotExist:
        raise Http404()
    task.delete()
    return redirect('/')
