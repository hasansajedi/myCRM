import arrow
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from common.models import Address
from common.utils import CURRENCY_CODES
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class InvoiceQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter()

    def search(self, query):
        lookups = (Q(first_name__icontains=query) |
                   Q(last_name__icontains=query) |
                   Q(email__icontains=query))
        return self.filter(lookups).distinct()


class InvoiceManager(models.Manager):
    def get_queryset(self):
        return InvoiceQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def disable_by_id(self, id):
        qs = Invoice.objects.get(id=id)
        if qs is not None:
            qs.deleted = True
            qs.is_active = False
            qs.save()
            return True
        else:
            return False

    def update_by_id(self, id, invoice_title, invoice_number, from_address, to_address, name, email, quantity, rate,
                     total_amount, currency, phone, amount_due, amount_paid, is_email_sent, status, details, due_date):
        qs = Invoice.objects.get(id=id)
        if qs is not None:
            qs.invoice_title = invoice_title
            qs.invoice_number = invoice_number
            qs.from_address = from_address
            qs.to_address = to_address
            qs.name = name
            qs.email = email
            qs.quantity = quantity
            qs.rate = rate
            qs.total_amount = total_amount
            qs.currency = currency
            qs.phone = phone
            qs.amount_due = amount_due
            qs.amount_paid = amount_paid
            qs.is_email_sent = is_email_sent
            qs.status = status
            qs.details = details
            qs.due_date = due_date
            qs.save()
            return True
        else:
            return False

    def remove_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            deleted, _rows_count = qs.delete()
            if deleted:
                return True
            else:
                return False
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Invoice(models.Model):
    INVOICE_STATUS = (
        ('Draft', 'Draft'),
        ('Sent', 'Sent'),
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancel'),
    )

    invoice_title = models.CharField(_('Invoice Title'), max_length=50)
    invoice_number = models.CharField(_('Invoice Number'), max_length=50)
    from_address = models.ForeignKey(Address, related_name='invoice_from_address', on_delete=models.SET_NULL, null=True)
    to_address = models.ForeignKey(Address, related_name='invoice_to_address', on_delete=models.SET_NULL, null=True)
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    # assigned_to = models.ManyToManyField(User, related_name='invoice_assigned_to')
    # quantity is the number of hours worked
    quantity = models.PositiveIntegerField(default=0)
    # rate is the rate charged
    rate = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    # total amount is product of rate and quantity
    total_amount = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CODES, blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='invoice_created_by',
                                   on_delete=models.SET_NULL, null=True)

    amount_due = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)
    is_email_sent = models.BooleanField(default=False)
    status = models.CharField(choices=INVOICE_STATUS,
                              max_length=15, default="Draft")
    details = models.TextField(_('Details'), null=True, blank=True)
    due_date = models.DateField(blank=True, null=True)

    # accounts = models.ManyToManyField(Account, related_name='accounts_invoices')
    # teams = models.ManyToManyField(Teams, related_name='invoices_teams')

    class Meta:
        """Meta definition for Invoice."""

        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        """Unicode representation of Invoice."""
        return self.invoice_number

    def formatted_total_amount(self):
        return self.currency + ' ' + str(self.total_amount)

    def formatted_rate(self):
        return str(self.rate) + ' ' + self.currency

    def formatted_total_quantity(self):
        return str(self.quantity) + ' ' + 'Hours'

    def is_draft(self):
        if self.status == 'Draft':
            return True
        else:
            return False

    def is_sent(self):
        if self.status == 'Sent' and self.is_email_sent == False:
            return True
        else:
            return False

    def is_resent(self):
        if self.status == 'Sent' and self.is_email_sent == True:
            return True
        else:
            return False

    def is_paid_or_cancelled(self):
        if self.status in ['Paid', 'Cancelled']:
            return True
        else:
            return False

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()
