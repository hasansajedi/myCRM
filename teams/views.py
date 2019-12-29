from collections import Set

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from teams.forms import TeamForm
from teams.models import Teams
from users.models import User

# from teams.tasks import update_team_users

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def load_data(r):
    context = {}
    if r.user.is_superuser:
        queryset = Teams.objects.all()
        users = User.objects.all()
        context['teams'] = queryset
        context['users'] = users
        return context
    else:
        raise PermissionDenied


@login_required
def teams_list(request):
    ctx = load_data(request)
    return render(request, 'teams/show.html', ctx)


@login_required
def team_create(request):
    context = {}
    if request.user.is_superuser:
        teams = Teams.objects.all()
        context['teams'] = teams
    else:
        raise PermissionDenied

    if request.method == 'GET':
        context['form'] = TeamForm()
        return render(request, 'teams/new.html', context)

    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            # obj.picture = request.FILES['picture']
            # obj.picture = request.POST['picture']
            # file_type = obj.picture.url.split('.')[-1]
            # if file_type.lower() not in IMAGE_FILE_TYPES:
            #     return render(request, 'profile_maker/error.html')
            obj.save()
            obj.users.set(User.objects.filter(id__in=request.POST.getlist('users')))
            form.save_m2m()
            return redirect('/teams/')

    # context = {"form": form, }
    # return render(request, 'teams/new.html', context)

    # if request.method == 'POST':
    #     form = TeamForm(request.POST)
    #     if form.is_valid():
    #         obj = form.save(commit=False)
    #         obj.created_by = request.user
    #         obj.picture = form.cleaned_data['picture']
    #         obj.save()
    #         obj.users.set(User.objects.filter(id__in=request.POST.getlist('users')))
    #         form.save_m2m()
    #
    #         # return JsonResponse({'error': False, 'success_url': reverse('teams:list')})
    #         return redirect('/teams/')
    #     else:
    #         # return JsonResponse({'error': True, 'errors': form.errors})
    #         err = form.errors
    #         return render(request, 'teams/new.html', {'form': form, 'error': err})


@login_required
def team_edit(request, id):
    if not (request.user.is_superuser):
        raise PermissionDenied
    team_obj = get_object_or_404(Teams, pk=id)
    if team_obj is not None:
        team_obj.users.set(User.objects.filter(username__in=request.POST.getlist('users')))
        team_obj.name = request.POST.get('name')
        team_obj.description = request.POST.get('description')
        team_obj.save()
        return redirect("/teams?updated=true")
    else:
        return render(request, 'teams/show.html', {'team': team_obj})


@login_required
def team_delete(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    team_obj = get_object_or_404(Teams, pk=id)
    print(team_obj)
    if request.method == 'GET':
        team_obj.delete()
        ctx = load_data(request)
        return render(request, 'teams/show.html', ctx)


@login_required
def search(request):
    q = request.POST.get('form_group_search_input', None)
    results = Teams.objects.filter(name__icontains=q, description__icontains=q)
    return render(request, "teams/show.html", {'teams': results})
