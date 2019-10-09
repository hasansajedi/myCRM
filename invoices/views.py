from django.db.models import Q
from django.shortcuts import render, redirect

from tasks.models import Task
from .forms import InvoiceForm
from .models import Invoice, InvoiceManager

INVOICE_STATUS = Invoice.INVOICE_STATUS


def new(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            try:
                form = form.save(commit=False)
                form.created_by = request.user
                form.save()
                return redirect('/invoices/')
            except:
                pass
        else:
            err = form.errors
            return render(request, 'invoices/new.html', {'form': form, 'error': err})
    else:
        form = InvoiceForm()
    return render(request, 'invoices/new.html', {'form': form,
                                                 'INVOICE_STATUS': INVOICE_STATUS})


def show(request):
    invoices = Invoice.objects.all().order_by('-id')
    active_count = invoices.filter().__len__()
    deleted_count = Invoice.objects.filter().__len__()

    show_deleted = (request.GET.get('show_deleted'))
    if show_deleted == 'true':
        deleted_invoices = Invoice.objects.filter(deleted=True)
        return render(request, "invoices/show.html", {'invoices': deleted_invoices,
                                                      'active_count': active_count,
                                                      'deleted_count': deleted_count,
                                                      'INVOICE_STATUS': INVOICE_STATUS})
    show_active = (request.GET.get('show_active'))
    if show_active == 'true':
        show_active = invoices.filter(is_active=True, deleted=False)
        return render(request, "invoices/show.html", {'invoices': show_active,
                                                      'active_count': active_count,
                                                      'deleted_count': deleted_count,
                                                      'INVOICE_STATUS': INVOICE_STATUS})

    return render(request, "invoices/show.html", {'invoices': invoices,
                                                  'active_count': active_count,
                                                  'deleted_count': deleted_count,
                                                  'INVOICE_STATUS': INVOICE_STATUS})


def search(request):
    q_keyword = request.POST.get('form_group_search_input', None)
    q_status = request.POST.get('form_group_status_input', None)

    lookups = Q(invoice_title__icontains=q_keyword)
    if q_keyword is not "":
        lookups = Q(invoice_title__icontains=q_keyword)
        if q_status is not "":
            lookups = Q(invoice_title__icontains=q_keyword) & (Q(status=q_status))
        else:
            pass
    elif q_status is not "":
        lookups = Q(status=q_status)
    else:
        invoices = Invoice.objects.all().order_by('-id')
        active_count = invoices.filter().__len__()
        deleted_count = Invoice.objects.filter().__len__()
        return render(request, "invoices/show.html", {'invoices': invoices,
                                                      'active_count': active_count,
                                                      'deleted_count': deleted_count,
                                                      'INVOICE_STATUS': INVOICE_STATUS})
    results = Invoice.objects.filter(lookups).distinct()
    return render(request, "invoices/show.html", {'invoices': results,
                                                  'INVOICE_STATUS': INVOICE_STATUS})


def edit(request, id):
    invoices = Invoice.objects.get(id=id)
    return render(request, 'invoices/edit.html', {'company': invoices})


def detail(request, id):
    company = Invoice.objects.get(id=id)
    tasks = Task.objects.filter(company=company)
    return render(request, 'invoices/detail.html', {'object': company,
                                                    'tasks': tasks,
                                                    'INVOICE_STATUS': INVOICE_STATUS})


def update(request, id):
    company = Invoice.objects.get(id=id)
    form = InvoiceForm(request.POST, instance=company)
    if form.is_valid():
        form.save()
        return redirect("/invoices?updated=true")
    else:
        err = form.errors
        print(err)
        return render(request, 'invoices/edit.html', {'company': company,
                                                      'errors': err,
                                                      'INVOICE_STATUS': INVOICE_STATUS})


def destroy(request, id):
    query = InvoiceManager.disable_by_id(InvoiceManager, id=id)
    if query:
        return redirect("/invoices?deleted=true")
    else:
        return redirect("/invoices?deleted=false")
