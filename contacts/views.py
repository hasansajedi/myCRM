from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import ListView, DetailView, View

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
        id = self.kwargs.get('pk')
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

def delete(request, id):
    query = ContactManager.disable_by_id(ContactManager,id=id)
    print(query)
    # query = Contact.objects.get(pk=person_pk)
    # query.delete()
    return HttpResponse("Deleted!")