import decimal

from django.http import JsonResponse

from payapp.models import Currency
from payapp.utils.banking import conversion_rates

# Create your views here.

def convert_amount(amount, currency1, currency2):
    return amount*conversion_rates[currency1][currency2]


def conversion_api(request, currency1, currency2, amount):
    # handle not supported currency
    currency1=str(currency1).upper()
    currency2=str(currency2).upper()
    if not request.method == 'GET' or not currency1 in Currency or not currency2 in Currency:
        error_data = {
            'success': False,
            'currency1': currency1,
            'currency2': currency2,
            'amount': amount,
            'error': f'unsupported conversion of {currency1} and {currency2}'
        }
        return JsonResponse(status=400, data=error_data)

    # convert amount if everything is right
    converted_amount = convert_amount(float(amount), currency1, currency2)

    data = {
        'success': True,
        'currency1': currency1,
        'currency2': currency2,
        'amount': amount,
        'converted_amount': converted_amount
    }
    return JsonResponse(status=200, data=data)