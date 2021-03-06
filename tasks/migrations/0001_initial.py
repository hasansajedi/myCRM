# Generated by Django 2.2.5 on 2019-10-16 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('status', models.CharField(choices=[('New', 'New'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=50, verbose_name='status')),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=50, verbose_name='priority')),
                ('task_type', models.CharField(blank=True, choices=[('Followup', 'Followup'), ('Call', 'Call'), ('Session', 'Session'), ('Send email', 'Send_email'), ('Send message', 'Send_message')], max_length=50, null=True, verbose_name='task_type')),
                ('due_date', models.DateField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('is_active', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=False, null=True)),
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, null=True, unique=True)),
                ('company', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='companies_tasks', to='companies.Company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-due_date'],
            },
        ),
    ]
