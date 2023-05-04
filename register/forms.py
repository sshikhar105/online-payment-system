from django import forms

from conversion_api.views import convert_amount
from register.models import UserAccount
from register.utils import check_username_exists
from payapp.models import Currency


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your username', 'class': 'form-control mt-2'}
    ), required=True)
    password = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your password', 'class': 'form-control mt-2', 'type': 'password'}
    ), required=True)

    def get_username(self):
        return self.cleaned_data['username']

    def get_password(self):
        return self.cleaned_data['password']


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your username', 'class': 'form-control mt-2'}
    ), required=True)
    password = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your password', 'class': 'form-control mt-2', 'type': 'password'}
    ), required=True)
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your Email', 'class': 'form-control mt-2'}
    ), required=True)
    firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your Firstname', 'class': 'form-control mt-2'}
    ), required=True)
    lastname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your Lastname', 'class': 'form-control mt-2'}
    ), required=True)
    currency = forms.ChoiceField(choices=Currency.choices, widget=forms.Select(
        attrs={'placeholder': 'Select Currency',
               'class': 'form-control mt-2'
               }
    ))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        input_username = cleaned_data.get('username')

        if check_username_exists(input_username):
            print('username exists')
            self.add_error(None, forms.ValidationError('This username is taken'))

    def save(self):
        username = self.cleaned_data['username']
        firstname = self.cleaned_data['firstname']
        lastname = self.cleaned_data['lastname']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        currency= self.cleaned_data['currency']
        converted_rate = convert_amount(1000,currency,Currency.GBP)
        user = UserAccount.objects.create_user(username, email, password, first_name=firstname, last_name=lastname,base_currency=currency,account_balance=converted_rate)
        user.save()
        return user


class RegisterAdminForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your username', 'class': 'form-control mt-2'}
    ), required=True)
    password = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your password', 'class': 'form-control mt-2', 'type': 'password'}
    ), required=True)
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your Email', 'class': 'form-control mt-2'}
    ), required=True)
    firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your Firstname', 'class': 'form-control mt-2'}
    ), required=True)
    lastname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your Lastname', 'class': 'form-control mt-2'}
    ), required=True)

    def __init__(self, *args, **kwargs):
        super(RegisterAdminForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        input_username = cleaned_data.get('username')

        if check_username_exists(input_username):
            print('username exists')
            self.add_error(None, forms.ValidationError('This username is taken'))

    def save(self):
        username = self.cleaned_data['username']
        firstname = self.cleaned_data['firstname']
        lastname = self.cleaned_data['lastname']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = UserAccount.objects.create_superuser(username, email, password, first_name=firstname, last_name=lastname)
        user.save()
        return user
