from django.conf.urls import url
from django.urls import path

from contacts import views
from .views import (
    ContactListView,
    ContactDetailSlugView,
    ContactDetailSlugEdit,
    delete_contact,
    # update_contact,
    editcontact,
    # ContactView,
)

urlpatterns = [
    # url(r'list$', ContactListView.as_view(), name='list'),
    #url(r'^delete/(?P<id>.*)$', delete_contact, name='delete'),
    #url(r'^update/(?P<id>.*)$', update_contact, name='update'),
    # url(r'^view/(?P<id>.*)$', ContactDetailSlugView.as_view(), name='view'),
    # url(r'^edit/(?P<id>.*)$', ContactDetailSlugEdit.as_view(), name='edit'),
    # url(r'^(?P<id>\d+)/edit/$', editcontact, name='edit'),
    # path('update/<int:pk>/', ContactView.as_view(), name='author-update'),
    path(r'emp', views.emp),
    path(r'', views.show, name='list'),
    path(r'edit/<int:id>', views.edit, name='edit'),
    path(r'update/<int:id>', views.update, name='update'),
    path(r'delete/<int:id>', views.destroy, name='delete'),
    path(r'search/', views.search, name='search'),
]
