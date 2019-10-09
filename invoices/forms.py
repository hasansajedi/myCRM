from django import forms
from .models import Invoice


class InvoiceForm(forms.ModelForm):
    teams_queryset = []
    teams = forms.MultipleChoiceField(choices=teams_queryset)

    def __init__(self, *args, **kwargs):
        # request_user = kwargs.pop('request_user', None)
        # assigned_users = kwargs.pop('assigned_to', [])
        super(InvoiceForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
            field.required = False

        # self.fields["teams"].required = False
        self.fields['invoice_number'].widget.attrs.update({'placeholder': 'inv-001'})
        self.fields['phone'].widget.attrs.update({'placeholder': '+91-123-456-7890'})
        self.fields['invoice_title'].required = True
        self.fields['invoice_number'].required = True
        self.fields['currency'].required = True
        self.fields['email'].required = True
        self.fields['total_amount'].required = True
        self.fields['due_date'].required = True

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if quantity in [None, '']:
            raise forms.ValidationError('This field is required')

        return quantity

    def clean_invoice_number(self):
        invoice_number = self.cleaned_data.get('invoice_number')
        if Invoice.objects.filter(invoice_number=invoice_number).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Invoice with this Invoice Number already exists.')
        return invoice_number

    class Meta:
        model = Invoice
        fields = ('invoice_title', 'invoice_number',
                  # 'from_address', 'to_address',
                  'name', 'company',
                  'email', 'phone', 'status',
                  'quantity', 'rate', 'total_amount',
                  'currency', 'details', 'due_date'
                  )