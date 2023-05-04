from django.shortcuts import render, redirect

from register.forms import RegisterAdminForm
from register.models import UserAccount
from payapp.decorators import admin_required
from payapp.forms import SendMoneyForm, RequestMoneyForm
from django import forms

from payapp.models import Transaction, MoneyRequest, MoneyRequestStatus, Notification
from payapp.utils.banking import transfer_money, send_money_request, approve_money_request, deny_money_request
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def index(request):
    if request.user.is_superuser:
        return index_admin(request)

    context = {
        'transactions': Transaction.objects.filter(
            Q(sender_id=request.user.id) |
            Q(recipient_id=request.user.id)
        ).order_by('-datetime').all()
    }
    return render(request, 'core/dashboard.html', context)


@login_required(login_url='login')
def send_money(request):
    form = SendMoneyForm(request.user)
    if request.method == 'POST':
        form = SendMoneyForm(request.user,request.POST)
        if form.is_valid():
            try:
                amount = form.get_amount()
                recipient = form.get_recipient()
                currency = form.get_currency()
                transfer_money(amount, request.user, recipient, currency)
                return render(request, 'core/send-money.html', {'form': SendMoneyForm(request.user), 'success': True})
            except Exception as e:
                form.add_error(None, forms.ValidationError(str(e)))

    return render(request, 'core/send-money.html', {'form': form})


@login_required(login_url='login')
def request_money(request):
    form = RequestMoneyForm(request.user)
    if request.method == 'POST':
        form = RequestMoneyForm(request.user,request.POST)
        if form.is_valid():
            try:
                amount = form.get_amount()
                recipient = form.get_recipient()
                currency = form.get_currency()
                send_money_request(amount, request.user, recipient, currency)
                return render(request, 'core/request-money.html', {'form': RequestMoneyForm(request.user), 'success': True})
            except Exception as e:
                form.add_error(None, forms.ValidationError(str(e)))

    return render(request, 'core/request-money.html', {'form': form})


@login_required(login_url='login')
def requests(request, message=None):
    context = {
        'requests': MoneyRequest.objects.filter(
            Q(recipient=request.user) &
            Q(status=MoneyRequestStatus.PENDING)
        ).all(),
        'message': message
    }
    return render(request, 'core/requests.html', context)


@login_required(login_url='login')
def approve_request(request):
    if not request.method == 'GET':
        raise Http404()
    if not request.GET.get('rid'):
        return redirect('requests')
    try:
        request_id = request.GET.get('rid')
        approve_money_request(request_id)
        return requests(request, {'message': 'Money request approved successfully', 'type': 'success'})
    except Exception as e:
        return requests(request, {'message': f'Could not approve money request. Error: {str(e)}', 'type': 'danger'})


@login_required(login_url='login')
def deny_request(request):
    if not request.method == 'GET':
        raise Http404()
    if not request.GET.get('rid'):
        return redirect('requests')
    try:
        request_id = request.GET.get('rid')
        deny_money_request(request_id)
        return requests(request, {'message': 'Money request denied successfully', 'type': 'success'})
    except Exception as e:
        return requests(request, {'message': f'Could not deny money request. Error: {str(e)}', 'type': 'danger'})


@login_required(login_url='login')
def notifications(request):
    context = {
        'notifications': Notification.objects.filter(
            Q(user=request.user)
        ).order_by('-datetime').all(),

    }
    return render(request, 'core/notifications.html', context)


@admin_required(login_url='login')
def index_admin(request):
    context = {
        'transactions': Transaction.objects.order_by('-datetime').all()[:10]
    }
    return render(request, 'core/dashboard-admin.html',context)

@admin_required(login_url='login')
def all_users(request):
    context = {
        'users': UserAccount.objects.order_by('-date_joined').all()
    }
    return render(request, 'core/all-users.html',context)

@admin_required(login_url='login')
def all_transactions(request):
    context = {
        'transactions': Transaction.objects.order_by('-datetime').all()[:10]
    }
    return render(request, 'core/all-transactions.html',context)

@admin_required(login_url='login')
def add_admin(request):
    form = RegisterAdminForm()
    if request.method == 'POST':
        form = RegisterAdminForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'core/add-admin.html', {'form': RegisterAdminForm(), 'message': {
                    'type': 'success',
                    'message': 'New Admin user created successfully'
                }})
            except Exception as e:
                return render(request, 'core/add-admin.html', {'form': RegisterAdminForm(), 'message': {
                    'type': 'danger',
                    'message': f'Could not create admin user. Error: {str(e)}'
                }})
    return render(request, 'core/add-admin.html', {'form': form})
