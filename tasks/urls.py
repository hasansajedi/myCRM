from django.urls import path

from .views import (
    new,
    show,
    edit,
    update,
    destroy,
    search,
    details,
    show_user_tasks,
    transfer_task,
    export_data,
)

urlpatterns = [
    path(r'', show, name='list'),
    path(r'new/', new, name='new'),
    path(r'edit/<int:id>', edit, name='edit'),
    path(r'transfer/<int:id>', transfer_task, name='transfer'),
    path(r'update/<int:id>', update, name='update'),
    path(r'delete/<int:id>', destroy, name='delete'),
    path(r'detail/<int:id>', details, name='detail'),
    path(r'report/<int:id>/<file_type>', export_data, name='report'),
    path(r'user-tasks/<username>', show_user_tasks, name='usertasks'),
    path(r'search/', search, name='search'),
]
