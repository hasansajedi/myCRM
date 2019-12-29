from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User
from crm.views import *


@login_required
@user_passes_test(lambda u: u.is_superuser)
def show(request):
    users = None
    if request.user.is_superuser:
        users = User.objects.all()
    elif request.user.is_staff:
        users = User.objects.filter(email=request.user.email)
    active_count = users.filter(is_active=True).__len__()

    show_deleted = (request.GET.get('show_deleted'))
    if show_deleted == 'true':
        deleted_users = User.objects.filter(is_active=False)
        return render(request, "users/show.html", {'users': deleted_users,
                                                   'active_count': active_count})
    elif (request.GET.get('show_active')) is not None:
        show_active = (request.GET.get('show_active'))
        if show_active == 'true':
            show_active = users.filter(is_active=True)
            return render(request, "users/show.html", {'users': show_active,
                                                       'active_count': active_count, })
    return render(request, "users/show.html", {'users': users,
                                               'active_count': active_count})


@login_required
def new(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/users/')
            except:
                pass
        else:
            err = form.errors
            print(err)
            return render(request, 'users/new.html', {'form': form, 'error': err})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/new.html', {'form': form})


@login_required
def search(request):
    q = request.POST.get('form_group_search_input', None)
    users = User.objects.filter(username__icontains=q)
    return render(request, "users/show.html", {'users': users})


@login_required
def edit(request, id):
    object = User.objects.get(id=id)
    return render(request, 'users/show.html', {'user': object})


@login_required
def show_profile(request, username):
    obj = None
    if username is not None:
        obj = User.objects.get(username=username)
    else:
        obj = User.objects.get(email=request.user.email)
    if obj is not None:
        return render(request, "users/detail.html", {'object': obj})
    else:
        login_user(request)


@login_required
def update(request, id):
    obj = None
    if id is not None:
        obj = User.objects.get(id=id)
    else:
        obj = User.objects.get(email=request.user.email)
    if obj is not None:
        form = CustomUserChangeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/users?updated=true")
        else:
            err = form.errors
            print(err)
            return render(request, 'users/detail.html', {'object': obj, 'errors': err})
    else:
        login_user(request)


@login_required
@staff_member_required
@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('login'))
def destroy(request, id):
    query = User.objects.get(id=id)
    if query.username != "admin":
        try:
            query.delete()
            return redirect("/users?deleted=true")
        except User.DoesNotExist:
            return redirect("/users?deleted=false")
        except Exception as e:
            return render(request, 'users/show.html', {'error': e.message})
    else:
        users = None
        if request.user.is_superuser:
            users = User.objects.all()
        elif request.user.is_staff:
            users = User.objects.filter(email=request.user.email)
        active_count = users.filter(is_active=True).__len__()

        show_deleted = (request.GET.get('show_deleted'))
        if show_deleted == 'true':
            deleted_users = User.objects.filter(is_active=False)
            return render(request, "users/show.html", {'users': deleted_users,
                                                       'active_count': active_count})
        elif (request.GET.get('show_active')) is not None:
            show_active = (request.GET.get('show_active'))
            if show_active == 'true':
                show_active = users.filter(is_active=True)
                return render(request, "users/show.html", {'users': show_active,
                                                           'active_count': active_count, })
        return render(request, "users/show.html", {'users': users,
                                                   'active_count': active_count,
                                                   'error': "You have not any permission to delete admin user."})
