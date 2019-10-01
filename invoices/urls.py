from django.urls import path

from .views import (
    new,
    show,
    edit,
    update,
    destroy,
    search,
    detail
)

urlpatterns = [
    path(r'', show, name='list'),
    path(r'new/', new, name='new'),
    path(r'edit/<int:id>', edit, name='edit'),
    path(r'update/<int:id>', update, name='update'),
    path(r'detail/<int:id>', detail, name='detail'),
    path(r'delete/<int:id>', destroy, name='delete'),
    path(r'search/', search, name='search'),
]
