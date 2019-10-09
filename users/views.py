from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

# Create your views here.
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User


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
    print(User._meta.fields)
    return render(request, "users/show.html", {'users': users,
                                               'active_count': active_count})


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


def search(request):
    q = request.POST.get('form_group_search_input', None)
    users = User.objects.filter(name__icontains=q)
    return render(request, "users/show.html", {'users': users})


def edit(request, id):
    companies = User.objects.get(id=id)
    return render(request, 'tasks/edit.html', {'tasks': companies})


def update(request, id):
    company = User.objects.get(id=id)
    form = CustomUserChangeForm(request.POST, instance=company)
    if form.is_valid():
        form.save()
        return redirect("/tasks?updated=true")
    else:
        err = form.errors
        print(err)
        return render(request, 'tasks/show.html', {'task': company, 'errors': err})
    return render(request, 'tasks/show.html', {'task': company})


def destroy(request, id):
    # query = TaskManager.disable_by_id(TaskManager, id=id)
    # if query:
    #     return redirect("/tasks?deleted=true")
    # else:
    #     return redirect("/tasks?deleted=false")
    pass
