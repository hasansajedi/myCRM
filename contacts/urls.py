from django.conf.urls import url
from django.urls import path

from .views import (
    ContactListView,
    ContactDetailSlugView,
    delete)

urlpatterns = [
    url(r'list$', ContactListView.as_view(), name='list'),
    url(r'^delete/(?P<id>.*)$', delete, name='delete'),
    path('<int:pk>/', ContactDetailSlugView.as_view(), name='contact_detail'),
]
