from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, UpdateView

from contacts.forms import ContactForm
from contacts.models import ContactManager
from .mixins import ObjectViewedMixin
from django.http import Http404
from .models import Contact


class ContactListView(ListView):
    model = Contact
    paginate_by = 10
    queryset = Contact.objects.all()
    template_name = "contacts/list.html"

    def get_queryset(self, *args, **kwargs):
        if self.kwargs:
            return Contact.objects.filter(category=self.kwargs['category']).order_by('-created_on')
        else:
            query = Contact.objects.all().order_by('-created_on')
            return query


class ContactDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Contact.objects.all()
    template_name = "contacts/detail.html"

    def get_context_data(self, *args, **kwargs):
        request = self.request
        context = super(ContactDetailSlugView, self).get_context_data(*args, **kwargs)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        id = self.kwargs.get('id')
        try:
            instance = Contact.objects.get(id=id, is_active=True)
        except Contact.DoesNotExist:
            raise Http404("Not found...")
        except Contact.MultipleObjectsReturned:
            qs = Contact.objects.filter(id=id, is_active=True)
            instance = qs.first()
        except:
            raise Http404("Hmmmmmmm")

        return instance


class ContactDetailSlugEdit(ObjectViewedMixin, DetailView):
    queryset = Contact.objects.all()
    template_name = "contacts/snippets/edit.html"

    # def get_context_data(self, *args, **kwargs):
    #     request = self.request
    #     context = super(ContactDetailSlugEdit, self).get_context_data(*args, **kwargs)
    #     return context

    def get_object(self, *args, **kwargs):
        request = self.request
        id = self.kwargs.get('id')
        try:
            instance = Contact.objects.get(id=id, is_active=True)
        except Contact.DoesNotExist:
            raise Http404("Not found...")
        except Contact.MultipleObjectsReturned:
            qs = Contact.objects.filter(id=id, is_active=True)
            instance = qs.first()
        except:
            raise Http404("Hmmmmmmm")

        # return instance
        return render(request, 'contacts/snippets/edit.html', {'object': instance})


def delete_contact(request, id):
    query = ContactManager.disable_by_id(ContactManager, id=id)
    print(query)
    return HttpResponse("Deleted!")


def editcontact(request, id):
    instance = ''
    try:
        instance = Contact.objects.get(id=id, is_active=True)
    except Contact.DoesNotExist:
        raise Http404("Not found...")
    except Contact.MultipleObjectsReturned:
        qs = Contact.objects.filter(id=id, is_active=True)
        instance = qs.first()
    except:
        raise Http404("Hmmmmmmm")

    form = ContactForm(request.POST or None)
    context = {'form': form, 'object': instance}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, "You successfully updated the post")
        context = {'form': form}
        return render(request, 'contacts/snippets/edit.html', context)

    else:
        context = {'form': form,
                   'object': instance,
                   'error': 'The form was not updated successfully. Please enter in a title and content'}
        return render(request, 'contacts/snippets/edit.html', context)


def emp(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/contacts/list.html')
            except:
                pass
        else:
            err = form.errors
            return render(request, 'contacts/index.html', {'form': form, 'error': err})
    else:
        form = ContactForm()
    return render(request, 'contacts/index.html', {'form': form})


def show(request):
    paginate_by = 2
    contacts = Contact.objects.all()
    return render(request, "contacts/show.html", {'contacts': contacts})


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
        return redirect("/contacts/show?updated=true")
    else:
        err = form.errors
        return render(request, 'contacts/edit.html', {'contact': contact, 'errors': err})
    return render(request, 'contacts/edit.html', {'contact': contact})


def destroy(request, id):
    query = ContactManager.disable_by_id(ContactManager, id=id)
    if query:
        return redirect("/contacts/show?deleted=true")
    else:
        return redirect("/contacts/show?deleted=false")
