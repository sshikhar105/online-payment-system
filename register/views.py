from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login as _login, authenticate,logout as _logout
from register.forms import LoginForm, RegisterForm
from django.forms import ValidationError

from register.models import UserAccount


# Create your views here.
def register(request):
    create_admin_if_not_found()
    form=RegisterForm()
    if request.method =='POST':
        print('POST request')
        form=RegisterForm(request.POST)
        if form.is_valid():
            print('form is valid')



            form.save()
            return redirect('login')
        else:
            print('invalid form')
            print(form.errors)
            return render(request, 'authentication/register.html', {'form': form})
    return render(request, 'authentication/register.html', {'form': form})


def login(request):
    create_admin_if_not_found()
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.get_username()
            password = form.get_password()
            user = authenticate(request, username=username, password=password)
            if not user is None:
                _login(request,user=user)
                return redirect('dashboard')
            else:
                form.add_error(None, ValidationError('Incorrect username or password'))
                return render(request, 'authentication/login.html', {'form': form})

    return render(request, 'authentication/login.html', {'form': form})


def logout(request):
    _logout(request)
    return redirect('login')

def create_admin_if_not_found():
    if UserAccount.objects.filter(username='admin1').exists():
        return
    else:
        UserAccount.objects.create_superuser(username='admin1',
                                             password='admin1')
