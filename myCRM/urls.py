from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(('crm.urls', 'crm'), namespace='crm')),
    url(r'^contacts/', include(('contacts.urls', 'contacts'), namespace='contacts')),
    url(r'^companies/', include(('companies.urls', 'companies'), namespace='companies')),
    url(r'^tasks/', include(('tasks.urls', 'tasks'), namespace='tasks')),
    url(r'^invoices/', include(('invoices.urls', 'invoices'), namespace='invoices')),
    url(r'^users/', include(('users.urls', 'users'), namespace='users')),
    url(r'^teams/', include(('teams.urls', 'teams'), namespace='teams')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'crm.views.not_found'
handler500 = 'crm.views.server_error'
