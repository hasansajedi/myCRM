from django.conf.urls import url

from .views import (
    ContactListView,
    ContactDetailSlugView,
    contact_detail)

urlpatterns = [
    url(r'$', ContactListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', ContactDetailSlugView.as_view(), name='detail'),
    url(r'^$', contact_detail, name="contact_detail"),
]
