from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from companies.models import Company
from contacts.models import Contact
from tasks.models import Task


def show(request):
    tasks_count = Task.objects.all().__len__()
    today_tasks = Task.objects.all().filter(deleted=False, is_active=True, due_date='2019-09-30')[:5]
    last_tasks = Task.objects.all().filter(deleted=False, is_active=True)[:5]

    contacts_count = Contact.objects.all().__len__()
    companies_count = Company.objects.all().__len__()

    return render(request, "crm/index.html", {'tasks_count': tasks_count,
                                              'contacts_count': contacts_count,
                                              'companies_count': companies_count,
                                              'last_tasks': last_tasks,
                                              'today_tasks':today_tasks})
