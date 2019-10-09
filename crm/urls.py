from django.urls import path

from .views import (
    show,
    login_user,
    logout_user,
)

urlpatterns = [
    path(r'', show, name='home'),
    path(r'login/', login_user, name='login'),
    path(r'logout/', logout_user, name='logout'),
]