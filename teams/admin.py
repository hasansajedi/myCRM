from django.contrib import admin

from .models import Teams


class TeamsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'description', ]

    class Meta:
        model = Teams

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Teams, TeamsAdmin)
