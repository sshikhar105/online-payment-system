import decimal

from django import forms
from django.db.models import Q

from register.models import UserAccount
from payapp.models import Currency


class SendMoneyForm(forms.Form):
    amount = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Enter Amount',
                                                              'class': 'form-control mt-2',
                                                              'type': 'number'
                                                              }))
    recipient = forms.ModelChoiceField(widget=forms.Select(attrs={'placeholder': 'Select recipient',
                                                                  'class': 'form-control mt-2'
                                                                  }), required=True, queryset=None
                                       )
    currency = forms.ChoiceField(choices=Currency.choices, widget=forms.Select(
        attrs={'placeholder': 'Select Currency',
               'class': 'form-control mt-2'
               }
    ))

    def __init__(self, user: UserAccount, *args, **kwargs):
        super(SendMoneyForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].queryset = UserAccount.objects.filter(Q(is_superuser=False) & ~Q(id=user.id)).all()

    def get_amount(self):
        return decimal.Decimal(self.cleaned_data.get('amount'))

    def get_recipient(self):
        return self.cleaned_data.get('recipient')

    def get_currency(self):
        return self.cleaned_data.get('currency')


class RequestMoneyForm(forms.Form):
    amount = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Enter Amount',
                                                              'class': 'form-control mt-2',
                                                              'type': 'number'
                                                              }))
    recipient = forms.ModelChoiceField(widget=forms.Select(attrs={'placeholder': 'Select recipient',
                                                                  'class': 'form-control mt-2'
                                                                  }), required=True,queryset=None)
    currency = forms.ChoiceField(choices=Currency.choices, widget=forms.Select(
        attrs={'placeholder': 'Select Currency',
               'class': 'form-control mt-2'
               }
    ))

    def __init__(self, user: UserAccount, *args, **kwargs):
        super(RequestMoneyForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].queryset = UserAccount.objects.filter(Q(is_superuser=False) & ~Q(id=user.id)).all()

    def get_amount(self):
        return decimal.Decimal(self.cleaned_data.get('amount'))

    def get_recipient(self):
        return self.cleaned_data.get('recipient')

    def get_currency(self):
        return self.cleaned_data.get('currency')
