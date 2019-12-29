from users.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Q
from shortuuidfield import ShortUUIDField

# from .utils import ContactsIndex


class ContactQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True, deleted=False)

    def search(self, query):
        lookups = (Q(first_name__icontains=query) |
                   Q(last_name__icontains=query) |
                   Q(email__icontains=query))
        return self.filter(lookups).distinct()


class ContactManager(models.Manager):
    def get_queryset(self):
        return ContactQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def disable_by_id(self, id):
        qs = Contact.objects.get(id=id)
        if qs is not None:
            qs.deleted = True
            qs.is_active = False
            qs.save()
            return True
        else:
            return False

    def update_by_id(self, id, first_name, last_name, email, phone, address, description, is_active):
        qs = Contact.objects.get(id=id)
        if qs is not None:
            qs.first_name = first_name
            qs.last_name = last_name
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


class Contact(models.Model):
    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(null=True, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # assigned_to = models.ManyToManyField(User, related_name='contact_assigned_users')
    created_by = models.ForeignKey(User, related_name='contact_created_by', on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    is_active = models.BooleanField(default=False)
    deleted = models.BooleanField(null=True, default=False)
    uuid = ShortUUIDField(null=True, unique=True)

    objects = ContactManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        ordering = ['-created_on']

    @property
    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def __unicode__(self):
        return u'%s' % self.full_name

    def get_absolute_url(self):
        return reverse('contact_detail', args=[self.id])

    # @models.permalink
    # def get_update_url(self):
    #     return 'contact_update', [self.uuid]
    #
    # @models.permalink
    # def get_delete_url(self):
    #     return 'contact_delete', [self.id]
