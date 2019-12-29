from django.http import HttpResponse

from companies.models import Company
from .utils import File_Exporter
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from users.models import User
from .forms import TaskForm, Task_flowForm, TaskUpdateForm
from .models import TaskManager, Task_flow
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
    tasks, tasks_list = None, None
    if request.user.is_superuser:
        tasks = Task.objects.all().order_by('-id')
        tasks_list = Task.objects.all().order_by('-id')
    elif request.user.is_staff:
        tasks = Task.objects.filter(created_by=request.user.id, is_active=True)
        tasks_list = Task.objects.filter(created_by=request.user.id, is_active=True)

    paginator = Paginator(tasks_list, 3)  # 3 task in each page
    page = request.GET.get('page')
    try:
        tasks_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        tasks_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        tasks_list = paginator.page(paginator.num_pages)

    STATUS_CHOICES = Task.STATUS_CHOICES
    PRIORITY_CHOICES = Task.PRIORITY_CHOICES

    active_count = tasks.filter(is_active=True).__len__()
    today_count = tasks.filter(is_active=True).filter(due_date=datetime.today().strftime('%Y-%m-%d')).__len__()
    deleted_count = tasks.filter(deleted=True).__len__()
    users = User.objects.all()

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

    return render(request, "tasks/show.html", {'tasks': tasks_list,
                                               'active_count': active_count,
                                               'today_count': today_count,
                                               'deleted_count': deleted_count,
                                               'STATUS_CHOICES': STATUS_CHOICES,
                                               'PRIORITY_CHOICES': PRIORITY_CHOICES,
                                               'users': users})


@login_required
def show_user_tasks(request, username):
    user = User.objects.get(username=username)
    tasks = Task.objects.filter(functor=user.id)
    STATUS_CHOICES = Task.STATUS_CHOICES
    PRIORITY_CHOICES = Task.PRIORITY_CHOICES

    active_count = tasks.filter(is_active=True).__len__()
    today_count = tasks.filter(is_active=True).filter(due_date=datetime.today().strftime('%Y-%m-%d')).__len__()
    deleted_count = tasks.filter(deleted=True).__len__()

    return render(request, "tasks/usertasks.html", {'tasks': tasks,
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
def details(request, id):
    obj = None
    if id is not None:
        obj = Task.objects.get(id=id)
    else:
        pass
    if obj is not None:
        task_flow_list = Task_flow.objects.filter(task=obj).order_by('-created_on')
        return render(request, "tasks/detail.html", {'object': obj,
                                                     'task_flow_list': task_flow_list})
    else:
        pass


@login_required
def edit(request, id):
    companies = Task.objects.get(id=id)
    return render(request, 'tasks/edit.html', {'tasks': companies})


@login_required
def update(request, id):
    task = Task.objects.get(id=id)
    form = TaskUpdateForm(request.POST, instance=task)
    if form.is_valid():
        form.save()
        return redirect("/tasks?updated=true")
    else:
        err = form.errors
        print(err)
        return render(request, 'tasks/show.html', {'task': task, 'errors': err})


@login_required
def transfer_task(request, id):
    task = Task.objects.get(id=id)
    if task is not None:
        form = Task_flowForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.transferred_by = request.user
            form.is_seen = False
            form.task = task
            form.save()

            task_functor = User.objects.get(username=request.POST.get("receiver"))
            TaskManager.change_functor(id=id, functor=task_functor, last_transferred_on=datetime.now())
            return redirect("/tasks?transferred=true")
        else:
            err = form.errors
            return render(request, 'tasks/show.html', {'task': task, 'errors': err})
    else:
        pass


@login_required
def destroy(request, id):
    query = TaskManager.disable_by_id(TaskManager, id=id)
    if query:
        return redirect("/tasks?deleted=true")
    else:
        return redirect("/tasks?deleted=false")


@login_required
def export_data(request, id, file_type):
    obj, task_flow_list, res = None, None, None
    if id is not None:
        obj = Task.objects.get(id=id)
    else:
        pass
    if obj is not None:
        if file_type == "xls":
            task_flow_list = Task_flow.objects.values_list('task', 'created_on', 'transferred_by',
                                                           'description').filter(
                task=obj).order_by('-created_on')
            ex = File_Exporter(columns=['Task', 'Created on', 'Transferred by', 'Description'], filename='workflow_',
                               file_type='xls')
            res = ex.generate_excel(data=task_flow_list, sheet_name='Workflow Data')
        elif file_type == "csv":
            task_flow_list = Task_flow.objects.filter(task=obj).order_by('-created_on')
            ex = File_Exporter(columns=['Task', 'Created on', 'Transferred by', 'Description'], filename='workflow_',
                               file_type='csv')
            res = ex.generate_csv(data=task_flow_list)
        elif file_type == "pdf":
            task_flow_list = Task_flow.objects.filter(task=obj).order_by('-created_on')
            data = {
                'today': datetime.today(),
                'task': obj.title,
                'data': task_flow_list,
                'user': request.user.username,
            }
            ex = File_Exporter(columns=['Task', 'Created on', 'Transferred by', 'Description'], filename='workflow_',
                               file_type='pdf')
            pdf = ex.generate_pdf('tasks/pdf_template.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        return (res)
    else:
        pass
