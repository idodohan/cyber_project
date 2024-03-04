import hashlib

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .forms import CustomUserCreationForm, CustomPasswordChangeForm
from .models import LoginAttempts, PasswordHistory


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists() or User.objects.filter(
                    username=form.cleaned_data['username']).exists():
                form = CustomUserCreationForm()
                return render(request, 'registration.html', {'form': form})
            form.save()
            user = User.objects.get(email=form.cleaned_data['email'])
            new_pass = PasswordHistory.objects.get_or_create(user=user, password_hash=user.password)
            new_pass.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
        if user is not None:
            attempts = LoginAttempts.objects.get_or_create(user=user)[0]
            if attempts.login_attempts < settings.PASSWORD_CONFIG.get('LOGIN_ATTEMPTS_LIMIT'):
                if not user.check_password(password):
                    attempts.login_attempts += 1
                    attempts.save()
                else:
                    attempts.login_attempts = 0
                    attempts.save()
                    user = authenticate(request, username=username, password=password)

                    if user is not None:
                        login(request, user)
                    return redirect('dashboard')
            else:
                messages.error(request, 'Too many consecutive failed login attempts. Your account is locked.')
                return redirect('account_locked_page')

            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    return render(request, 'login.html')


def change_password(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        form = CustomPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            attempts = LoginAttempts.objects.get_or_create(user=user)[0]
            attempts.login_attempts = 0
            attempts.save()
            new_pass = PasswordHistory.objects.get_or_create(user=user, password_hash=user.password)
            new_pass.save()
            return redirect('dashboard')
    else:
        user = User.objects.get(id=user_id)
        form = CustomPasswordChangeForm(user)
        login(request, user)
    return render(request, 'change_password.html', {'form': form, 'user_id': user_id})


def change_password_no_id(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = CustomPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            attempts = LoginAttempts.objects.get_or_create(user=user)[0]
            attempts.login_attempts = 0
            attempts.save()
            new_pass = PasswordHistory.objects.get_or_create(user=user, password_hash=user.password)
            new_pass.save()
            return redirect('dashboard')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form, 'user_id': request.user.id})


def account_locked_page(request):
    return render(request, 'account_locked_page.html')


def password_reset(request, step=0):
    if request.method == 'POST':
        user_email = request.session.get('reset_email', request.POST.get('email'))
        try:
            user = User.objects.get(email=user_email)
            match step:
                case 0:
                    pass

                case 1:
                    sha1_value = hashlib.sha1(str(user.pk).encode() + user.email.encode()).hexdigest()
                    user.sha1_value = sha1_value
                    user.set_password(sha1_value)
                    user.save()
                    send_mail('Password Reset', f'Your reset code: {sha1_value}', 'from@example.com', [user_email],
                              fail_silently=False)
                    step += 1
                    return redirect('change_password', user_id=user.id)

                case 2:
                    sha1_value_from_form = request.POST.get('sha1_value')

                    if sha1_value_from_form == hashlib.sha1(str(user.pk).encode() + user.email.encode()).hexdigest():
                        step += 1
                        return redirect('change_password', user_id=user.id)


        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

    return render(request, 'forgot_password.html', {'step': 1})
