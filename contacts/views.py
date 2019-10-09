from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, UpdateView

from contacts.forms import ContactForm
from contacts.models import ContactManager
from django.http import Http404
from .models import Contact


def new(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                form = form.save(commit=False)
                form.created_by = request.user
                form.save()
                return redirect('/contacts')
            except:
                pass
        else:
            err = form.errors
            return render(request, 'contacts/index.html', {'form': form, 'error': err})
    else:
        form = ContactForm()
    return render(request, 'contacts/index.html', {'form': form})


def show(request):
    contacts = Contact.objects.all()
    active_count = contacts.filter(is_active=True).__len__()
    deleted_count = contacts.filter(deleted=True).__len__()

    show_deleted = (request.GET.get('show_deleted'))
    if show_deleted == 'true':
        deleted_contacts = contacts.filter(deleted=True)
        return render(request, "contacts/show.html", {'contacts': deleted_contacts,
                                                      'active_count': active_count,
                                                      'deleted_count': deleted_count})
    show_active = (request.GET.get('show_active'))
    if show_active == 'true':
        show_active = contacts.filter(is_active=True, deleted=False)
        return render(request, "contacts/show.html", {'contacts': show_active,
                                                      'active_count': active_count,
                                                      'deleted_count': deleted_count})

    return render(request, "contacts/show.html", {'contacts': contacts,
                                                  'active_count': active_count,
                                                  'deleted_count': deleted_count})


def search(request):
    q = request.POST.get('form_group_search_input', None)
    contacts = Contact.objects.filter(first_name__icontains=q, last_name__icontains=q, email__icontains=q)
    return render(request, "contacts/show.html", {'contacts': contacts})


def edit(request, id):
    contacts = Contact.objects.get(id=id)
    return render(request, 'contacts/edit.html', {'contact': contacts})


def update(request, id):
    contact = Contact.objects.get(id=id)
    form = ContactForm(request.POST, instance=contact)
    if form.is_valid():
        form.save()
        return redirect("/contacts?updated=true")
    else:
        err = form.errors
        return render(request, 'contacts/edit.html', {'contact': contact, 'errors': err})
    return render(request, 'contacts/edit.html', {'contact': contact})


def destroy(request, id):
    query = ContactManager.disable_by_id(ContactManager, id=id)
    if query:
        return redirect("/contacts?deleted=true")
    else:
        return redirect("/contacts?deleted=false")
