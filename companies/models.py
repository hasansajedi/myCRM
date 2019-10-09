from users.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Q
from shortuuidfield import ShortUUIDField


class CompanyQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True, deleted=False)

    def search(self, query):
        lookups = (Q(first_name__icontains=query) |
                   Q(last_name__icontains=query) |
                   Q(email__icontains=query))
        return self.filter(lookups).distinct()


class CompanyManager(models.Manager):
    def get_queryset(self):
        return CompanyQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def disable_by_id(self, id):
        qs = Company.objects.get(id=id)
        if qs is not None:
            qs.deleted = True
            qs.is_active = False
            qs.save()
            return True
        else:
            return False

    def update_by_id(self, id, name, manager_name, website, email, phone, address, description, is_active):
        qs = Company.objects.get(id=id)
        if qs is not None:
            qs.name = name
            qs.manager_name = manager_name
            qs.website = website
            qs.email = email
            qs.phone = phone
            qs.address = address
            qs.description = description
            qs.is_active = is_active
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


class Company(models.Model):
    name = models.CharField(_("Company name"), max_length=255)
    manager_name = models.CharField(_("Company manager name"), null=True, max_length=255)
    website = models.URLField(null=True)
    email = models.EmailField(null=True)
    phone = PhoneNumberField(null=True)
    address = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    # assigned_to = models.ManyToManyField(User, related_name='contact_assigned_users')
    created_by = models.ForeignKey(User, related_name='company_created_by', on_delete=models.SET_NULL, null=True)
    createdon = models.DateTimeField(_("Created on"), auto_now_add=True)
    is_active = models.BooleanField(default=True)
    deleted = models.BooleanField(null=True, default=False)
    uuid = ShortUUIDField(null=True, unique=True)

    objects = CompanyManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-createdon']

    def __unicode__(self):
        return u'%s' % self.name