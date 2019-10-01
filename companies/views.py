from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, UpdateView

from tasks.models import Task
from .forms import CompanyForm
from .models import CompanyManager
from django.http import Http404
from .models import Company


def new(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/companies/')
            except:
                pass
        else:
            err = form.errors
            return render(request, 'companies/show.html', {'formNew': form, 'error': err})
    else:
        form = CompanyForm()
    return render(request, 'companies/new.html', {'form': form})


def show(request):
    companies = Company.objects.all()
    active_count = companies.filter(is_active=True).__len__()
    deleted_count = Company.objects.filter(deleted=True).__len__()

    show_deleted = (request.GET.get('show_deleted'))
    if show_deleted == 'true':
        deleted_companies = Company.objects.filter(deleted=True)
        return render(request, "companies/show.html", {'companies': deleted_companies,
                                                       'active_count': active_count,
                                                       'deleted_count': deleted_count})
    show_active = (request.GET.get('show_active'))
    if show_active == 'true':
        show_active = companies.filter(is_active=True, deleted=False)
        return render(request, "companies/show.html", {'companies': show_active,
                                                       'active_count': active_count,
                                                       'deleted_count': deleted_count})

    return render(request, "companies/show.html", {'companies': companies,
                                                   'active_count': active_count,
                                                   'deleted_count': deleted_count})


def search(request):
    q = request.POST.get('form_group_search_input', None)
    companies = Company.objects.filter(name__icontains=q)
    return render(request, "companies/show.html", {'companies': companies})


def edit(request, id):
    companies = Company.objects.get(id=id)
    return render(request, 'companies/edit.html', {'company': companies})


def detail(request, id):
    company = Company.objects.get(id=id)
    tasks = Task.objects.filter(company=company)
    return render(request, 'companies/detail.html', {'object': company,
                                                     'tasks': tasks})


def update(request, id):
    company = Company.objects.get(id=id)
    form = CompanyForm(request.POST, instance=company)
    if form.is_valid():
        form.save()
        return redirect("/companies?updated=true")
    else:
        err = form.errors
        print(err)
        return render(request, 'companies/edit.html', {'company': company, 'errors': err})
    return render(request, 'companies/edit.html', {'company': company})


def destroy(request, id):
    query = CompanyManager.disable_by_id(CompanyManager, id=id)
    if query:
        return redirect("/companies?deleted=true")
    else:
        return redirect("/companies?deleted=false")
