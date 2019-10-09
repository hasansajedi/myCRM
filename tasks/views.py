from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, UpdateView

from users.models import User
from .forms import TaskForm
from .models import TaskManager
from datetime import datetime
from .models import Task


@login_required
def new(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                form = form.save(commit=False)
                form.created_by = request.user
                form.save()
                return redirect('/tasks/')
            except:
                pass
        else:
            err = form.errors
            return render(request, 'tasks/new.html', {'form': form, 'error': err})
    else:
        form = TaskForm()
    return render(request, 'tasks/new.html', {'form': form})


@login_required
def show(request):
    tasks = None
    if request.user.is_superuser:
        tasks = Task.objects.all().order_by('-id')
    elif request.user.is_staff:
        tasks = Task.objects.filter(created_by=request.user.id, is_active=True)

    STATUS_CHOICES = Task.STATUS_CHOICES
    PRIORITY_CHOICES = Task.PRIORITY_CHOICES

    active_count = tasks.filter(is_active=True).__len__()
    today_count = tasks.filter(is_active=True).filter(due_date=datetime.today().strftime('%Y-%m-%d')).__len__()
    deleted_count = Task.objects.filter(deleted=True).__len__()

    show_deleted = (request.GET.get('show_deleted'))
    if show_deleted == 'true':
        deleted_companies = Task.objects.filter(deleted=True)
        return render(request, "tasks/show.html", {'tasks': deleted_companies,
                                                   'active_count': active_count,
                                                   'today_count': today_count,
                                                   'deleted_count': deleted_count,
                                                   'STATUS_CHOICES': STATUS_CHOICES,
                                                   'PRIORITY_CHOICES': PRIORITY_CHOICES})
    elif (request.GET.get('show_active')) is not None:
        show_active = (request.GET.get('show_active'))
        if show_active == 'true':
            show_active = tasks.filter(is_active=True, deleted=False)
            return render(request, "tasks/show.html", {'tasks': show_active,
                                                       'active_count': active_count,
                                                       'today_count': today_count,
                                                       'deleted_count': deleted_count,
                                                       'STATUS_CHOICES': STATUS_CHOICES,
                                                       'PRIORITY_CHOICES': PRIORITY_CHOICES})
    elif (request.GET.get('show_today')) is not None:
        show_today = (request.GET.get('show_today'))
        if show_today == 'true':
            show_today = tasks.filter(is_active=True, deleted=False).filter(
                due_date=datetime.today().strftime('%Y-%m-%d'))
            return render(request, "tasks/show.html", {'tasks': show_today,
                                                       'active_count': active_count,
                                                       'today_count': today_count,
                                                       'deleted_count': deleted_count,
                                                       'STATUS_CHOICES': STATUS_CHOICES,
                                                       'PRIORITY_CHOICES': PRIORITY_CHOICES})

    return render(request, "tasks/show.html", {'tasks': tasks,
                                               'active_count': active_count,
                                               'today_count': today_count,
                                               'deleted_count': deleted_count,
                                               'STATUS_CHOICES': STATUS_CHOICES,
                                               'PRIORITY_CHOICES': PRIORITY_CHOICES})


@login_required
def search(request):
    q = request.POST.get('form_group_search_input', None)
    companies = Task.objects.filter(name__icontains=q)
    return render(request, "tasks/show.html", {'tasks': companies})


@login_required
def edit(request, id):
    companies = Task.objects.get(id=id)
    return render(request, 'tasks/edit.html', {'tasks': companies})


@login_required
def update(request, id):
    company = Task.objects.get(id=id)
    form = TaskForm(request.POST, instance=company)
    if form.is_valid():
        form.save()
        return redirect("/tasks?updated=true")
    else:
        err = form.errors
        return render(request, 'tasks/show.html', {'task': company, 'errors': err})
    return render(request, 'tasks/show.html', {'task': company})


@login_required
def destroy(request, id):
    query = TaskManager.disable_by_id(TaskManager, id=id)
    if query:
        return redirect("/tasks?deleted=true")
    else:
        return redirect("/tasks?deleted=false")
