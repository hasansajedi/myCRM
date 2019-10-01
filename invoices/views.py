from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, UpdateView

from tasks.models import Task
from .forms import InvoiceForm
from django.http import Http404
from .models import Invoice, InvoiceManager


def new(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/invoices/')
            except:
                pass
        else:
            err = form.errors
            return render(request, 'invoices/show.html', {'formNew': form, 'error': err})
    else:
        form = InvoiceForm()
    return render(request, 'invoices/new.html', {'form': form})


def show(request):
    invoices = Invoice.objects.all()
    active_count = invoices.filter(is_active=True).__len__()
    deleted_count = Invoice.objects.filter(deleted=True).__len__()

    show_deleted = (request.GET.get('show_deleted'))
    if show_deleted == 'true':
        deleted_invoices = Invoice.objects.filter(deleted=True)
        return render(request, "invoices/show.html", {'invoices': deleted_invoices,
                                                       'active_count': active_count,
                                                       'deleted_count': deleted_count})
    show_active = (request.GET.get('show_active'))
    if show_active == 'true':
        show_active = invoices.filter(is_active=True, deleted=False)
        return render(request, "invoices/show.html", {'invoices': show_active,
                                                       'active_count': active_count,
                                                       'deleted_count': deleted_count})

    return render(request, "invoices/show.html", {'invoices': invoices,
                                                   'active_count': active_count,
                                                   'deleted_count': deleted_count})


def search(request):
    q = request.POST.get('form_group_search_input', None)
    invoices = Invoice.objects.filter(name__icontains=q)
    return render(request, "invoices/show.html", {'invoices': invoices})


def edit(request, id):
    invoices = Invoice.objects.get(id=id)
    return render(request, 'invoices/edit.html', {'company': invoices})


def detail(request, id):
    company = Invoice.objects.get(id=id)
    tasks = Task.objects.filter(company=company)
    return render(request, 'invoices/detail.html', {'object': company,
                                                     'tasks': tasks})


def update(request, id):
    company = Invoice.objects.get(id=id)
    form = InvoiceForm(request.POST, instance=company)
    if form.is_valid():
        form.save()
        return redirect("/invoices?updated=true")
    else:
        err = form.errors
        print(err)
        return render(request, 'invoices/edit.html', {'company': company, 'errors': err})
    return render(request, 'invoices/edit.html', {'company': company})


def destroy(request, id):
    query = InvoiceManager.disable_by_id(InvoiceManager, id=id)
    if query:
        return redirect("/invoices?deleted=true")
    else:
        return redirect("/invoices?deleted=false")
