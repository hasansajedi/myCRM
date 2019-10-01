from django.urls import path

from .views import (
    show,
)

urlpatterns = [
    path(r'', show, name='home'),
]
