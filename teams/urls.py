from django.urls import path
from teams.views import (
    teams_list,
    team_create,
    team_edit,
    team_delete,
    search,
    team_edit,
)

app_name = 'teams'

urlpatterns = [
    path('', teams_list, name='list'),
    path('new/', team_create, name='new'),
    path('edit/<int:id>/', team_edit, name='update'),
    path('delete/<int:id>/', team_delete, name='delete'),
    # path('detail/<int:id>/', team_detail, name='detail'),
    path(r'update/<int:id>', team_edit, name='update'),
    path(r'search/', search, name='search'),
]
