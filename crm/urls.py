from django.urls import path

from .views import (
    show,
    login_user,
    logout_user,
    has_been_seen,
)

urlpatterns = [
    path(r'', show, name='home'),
    path(r'login/', login_user, name='login'),
    path(r'logout/', logout_user, name='logout'),
    path(r'has_been_seen/<int:id>', has_been_seen, name='has_been_seen'),
]
