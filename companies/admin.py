from django.contrib import admin

from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'manager_name', 'email', 'created_by', 'phone', 'is_active', 'deleted']

    class Meta:
        model = Company


admin.site.register(Company, CompanyAdmin)
