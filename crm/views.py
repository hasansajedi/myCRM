from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from companies.models import Company
from contacts.models import Contact
from events.models import Event
from invoices.models import Invoice
from tasks.models import Task, Task_flow, Task_flowManager

from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime

from teams.models import Teams
from users.models import User


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['user_name']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    context = {'foo': 'bar'}
    return render(request, 'registration/login.html', context)


def logout_user(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return HttpResponseRedirect('/login')


def get_data(user_type, user_id):
    contacts_count = companies_count = invoices_count = tasks_count = teams_count = events_count = 0
    last_tasks = today_tasks = tasks_flow = None
    user = User.objects.get(id=user_id)
    if user_type == "superuser":
        teams_count = Teams.objects.all().__len__()
        events_count = Event.objects.filter(disabled=False, is_active=True).__len__()
        tasks_count = Task.objects.filter(deleted=False, is_active=True).__len__()
        today_tasks = Task.objects.filter(deleted=False, is_active=True,
                                          due_date=datetime.today().strftime('%Y-%m-%d'))
        last_tasks = Task.objects.filter(deleted=False, is_active=True)[:5]

        functors_tasks = Task.objects.filter(functor=user.id)
        tasks_flow = Task_flow.objects.filter(task__in=functors_tasks, is_seen=False)

        contacts_count = Contact.objects.all().__len__()
        companies_count = Company.objects.all().__len__()
        invoices_count = Invoice.objects.all().__len__()

    elif user_type == "staff":
        teams_count = Teams.objects.all().__len__()
        events_count = Event.objects.filter(disabled=False, is_active=True).__len__()

        tasks_count = Task.objects.filter(created_by=user.id, is_active=True, deleted=False).__len__()
        today_tasks = Task.objects.filter(created_by=user.id, deleted=False, is_active=True,
                                          due_date=datetime.today().strftime('%Y-%m-%d'))
        last_tasks = Task.objects.filter(created_by=user.id, deleted=False, is_active=True)[:5]

        functors_tasks = Task.objects.filter(functor=user.id)
        tasks_flow = Task_flow.objects.filter(task__in=functors_tasks, is_seen=False)

        contacts_count = Contact.objects.filter(created_by=user.id).__len__()
        companies_count = Company.objects.filter(created_by=user.id).__len__()
        invoices_count = Invoice.objects.filter(created_by=user.id).__len__()
    return {'tasks_count': tasks_count,
            'today_tasks': today_tasks,
            'last_tasks': last_tasks,
            'tasks_flow': tasks_flow,
            'contacts_count': contacts_count,
            'companies_count': companies_count,
            'invoices_count': invoices_count,
            'teams_count': teams_count,
            'events_count': events_count, }


@login_required
def show(request):
    storage = messages.get_messages(request)
    storage.used = True
    data = None
    if request.user.is_superuser:
        data = get_data('superuser', user_id=request.user.id)
    elif request.user.is_staff:
        data = get_data('staff', user_id=request.user.id)

    return render(request, "crm/index.html", {'tasks_count': data.get('tasks_count'),
                                              'contacts_count': data.get('contacts_count'),
                                              'companies_count': data.get('companies_count'),
                                              'last_tasks': data.get('last_tasks'),
                                              'today_tasks': data.get('today_tasks'),
                                              'invoices_count': data.get('invoices_count'),
                                              'tasks_flow': data.get('tasks_flow'),
                                              'teams_count': data.get('teams_count'),
                                              'events_count': data.get('events_count'),
                                              })


@login_required
def has_been_seen(request, id):
    ts = Task_flowManager()
    x = ts.has_been_seen(id)
    if x:
        data = None
        if request.user.is_superuser:
            data = get_data('superuser', user_id=request.user.id)
        elif request.user.is_staff:
            data = get_data('staff', user_id=request.user.id)
        messages.success(request, "Your data has been saved!")
        return HttpResponseRedirect('/')

        # return render(request, "crm/index.html", {'tasks_count': data.get('tasks_count'),
        #                                           'contacts_count': data.get('contacts_count'),
        #                                           'companies_count': data.get('companies_count'),
        #                                           'last_tasks': data.get('last_tasks'),
        #                                           'today_tasks': data.get('today_tasks'),
        #                                           'invoices_count': data.get('invoices_count'),
        #                                           'tasks_flow': data.get('tasks_flow')})
    else:
        show(request)


def not_found(request, exception=None):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def server_error(request, exception=None):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
