from django.contrib import admin

from .models import Task


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'status', 'priority', 'due_date', 'created_on', 'created_by', 'is_active', 'deleted']

    class Meta:
        model = Task


admin.site.register(Task, CompanyAdmin)
