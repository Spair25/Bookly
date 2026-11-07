from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, UserEditForm, ProfileEditForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    error = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        error = 'Invalid username or password.'

    return render(
        request,
        'users/login.html',
        {'error': error}
    )


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def profile_view(request):
    profile = request.user.profile

    return render(
        request,
        'users/profile.html',
        {
            'profile': profile,
        }
    )
@login_required(login_url='login')
def edit_profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        user_form = UserEditForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)

    return render(
        request,
        'users/edit_profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )