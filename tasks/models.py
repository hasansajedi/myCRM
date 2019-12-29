from users.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Q
from shortuuidfield import ShortUUIDField

from companies.models import Company
from contacts.models import Contact
import arrow


class TaskQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True, deleted=False)

    def search(self, query):
        lookups = (Q(first_name__icontains=query) |
                   Q(last_name__icontains=query) |
                   Q(email__icontains=query))
        return self.filter(lookups).distinct()


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def disable_by_id(self, id):
        qs = Task.objects.get(id=id)
        if qs is not None:
            qs.deleted = True
            qs.is_active = False
            qs.save()
            return True
        else:
            return False

    def update_by_id(self, id, title, status, priority, due_date, is_active):
        qs = Task.objects.get(id=id)
        if qs is not None:
            qs.title = title
            qs.status = status
            qs.priority = priority
            qs.due_date = due_date
            qs.is_active = is_active
            qs.save()
            return True
        else:
            return False

    @classmethod
    def change_functor(cls, id, functor, last_transferred_on):
        qs = Task.objects.get(id=id)
        if qs is not None:
            qs.functor = functor
            qs.last_transferred_on = last_transferred_on
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


class Task(models.Model):
    STATUS_CHOICES = (
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed")
    )
    PRIORITY_CHOICES = (
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High")
    )
    TYPE_CHOICES = (
        ("Followup", "Followup"),
        ("Call", "Call"),
        ("Session", "Session"),
        ("Send email", "Send_email"),
        ("Send message", "Send_message"),
    )

    title = models.CharField(_("title"), max_length=200)
    status = models.CharField(_("status"), max_length=50, choices=STATUS_CHOICES)
    priority = models.CharField(_("priority"), max_length=50, choices=PRIORITY_CHOICES)
    task_type = models.CharField(_("task_type"), max_length=50, blank=True, null=True, choices=TYPE_CHOICES)
    due_date = models.DateField(blank=True, null=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    company = models.ForeignKey(Company, default=None, related_name="companies_tasks", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='task_created', blank=True, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    deleted = models.BooleanField(null=True, default=False)
    uuid = ShortUUIDField(null=True, unique=True)
    functor = models.ForeignKey(User, related_name='task_functor', blank=True, null=True, on_delete=models.CASCADE)
    last_transferred_on = models.DateTimeField(_("Last transferred on"), blank=True, null=True)
    complete_date = models.DateField(blank=True, null=True)

    objects = TaskManager()

    def __str__(self):
        return self.title

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    class Meta:
        ordering = ['-due_date']

    def __unicode__(self):
        return u'%s' % self.title


class Task_flowQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = (Q(task__icontains=query) |
                   Q(description__icontains=query) |
                   Q(created_on__icontains=query))
        return self.filter(lookups).distinct()


class Task_flowManager(models.Manager):
    def get_queryset(self):
        return Task_flowQuerySet(self.model, using=self._db)

    def has_been_seen(self, id):
        print(id)
        qs = Task_flow.objects.get(id=id)
        if qs is not None:
            qs.is_seen = True
            qs.save()
            return True
        return False


class Task_flow(models.Model):
    task = models.ForeignKey(Task, related_name='task', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    transferred_by = models.ForeignKey(User, related_name='task_transferred', blank=True, null=True,
                                       on_delete=models.CASCADE)
    uuid = ShortUUIDField(null=True, unique=True)
    is_seen = models.BooleanField(default=False, null=True)

    objects = Task_flowManager()

    def __str__(self):
        return self.task.title

    def was_seen(self):
        return self.is_seen

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    class Meta:
        ordering = ['-created_on']

    def __unicode__(self):
        return u'%s' % self.task.title
