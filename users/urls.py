from django.urls import path

from .views import (
    new,
    show,
    edit,
    update,
    destroy,
    search,
    show_profile,
)

urlpatterns = [
    path(r'', show, name='list'),
    path(r'profile/<username>', show_profile, name='profile'),
    path(r'new/', new, name='new'),
    path(r'edit/<int:id>', edit, name='edit'),
    path(r'update/<int:id>', update, name='update'),
    path(r'delete/<int:id>', destroy, name='delete'),
    path(r'search/', search, name='search'),
]
