from django.shortcuts import render, get_object_or_404, redirect

from companies.models import Company
from contacts.models import Contact
from invoices.models import Invoice
from tasks.models import Task

from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime


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


@login_required
def show(request):
    contacts_count = companies_count = invoices_count = last_tasks = today_tasks = tasks_count = 0

    if request.user.is_superuser:
        tasks_count = Task.objects.filter(deleted=False, is_active=True).__len__()
        today_tasks = Task.objects.filter(deleted=False, is_active=True,
                                                due_date=datetime.today().strftime('%Y-%m-%d'))
        last_tasks = Task.objects.filter(deleted=False, is_active=True)[:5]
        contacts_count = Contact.objects.all().__len__()
        companies_count = Company.objects.all().__len__()
        invoices_count = Invoice.objects.all().__len__()

    elif request.user.is_staff:
        tasks_count = Task.objects.filter(created_by=request.user.id, is_active=True, deleted=False).__len__()
        today_tasks = Task.objects.filter(created_by=request.user.id, deleted=False, is_active=True,
                                                due_date=datetime.today().strftime('%Y-%m-%d'))
        last_tasks = Task.objects.filter(created_by=request.user.id, deleted=False, is_active=True)[:5]
        contacts_count = Contact.objects.filter(created_by=request.user.id).__len__()
        companies_count = Company.objects.filter(created_by=request.user.id).__len__()
        invoices_count = Invoice.objects.filter(created_by=request.user.id).__len__()

    return render(request, "crm/index.html", {'tasks_count': tasks_count,
                                              'contacts_count': contacts_count,
                                              'companies_count': companies_count,
                                              'last_tasks': last_tasks,
                                              'today_tasks': today_tasks,
                                              'invoices_count': invoices_count})


def not_found(request, exception=None):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def server_error(request, exception=None):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
