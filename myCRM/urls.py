from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(('crm.urls', 'crm'), namespace='crm')),
    url(r'^contacts/', include(('contacts.urls', 'contacts'), namespace='contacts')),
    url(r'^companies/', include(('companies.urls', 'companies'), namespace='companies')),
    url(r'^tasks/', include(('tasks.urls', 'tasks'), namespace='tasks')),
]
