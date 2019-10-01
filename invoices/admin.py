from django.contrib import admin

from .models import Invoice


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'invoice_title', 'invoice_number', 'from_address', 'to_address', 'name', 'email']

    class Meta:
        model = Invoice


admin.site.register(Invoice, InvoiceAdmin)
