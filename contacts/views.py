from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .mixins import ObjectViewedMixin
from django.http import Http404
from .models import Contact


class ContactListView(ListView):
    queryset = Contact.objects.all()
    template_name = "contacts/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Contact.objects.all()

def contact_detail(request, uuid):
    contact = Contact.objects.get(uuid=uuid)

    return render(request,
                'contacts/detail.html',
                {'obj': contact}
    )


