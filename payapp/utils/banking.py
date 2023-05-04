import decimal

from register.models import UserAccount
from .notification import notify
from ..models import Currency, Transaction, MoneyRequest, MoneyRequestStatus

conversion_rates = {
    'USD': {
        'GBP': 0.8,
        'EUR': 0.9,
        'USD': 1.0
    },
    'GBP': {
        'GBP': 1.0,
        'EUR': 1.1,
        'USD': 1.2
    },
    'EUR': {
        'GBP': 0.9,
        'EUR': 1.0,
        'USD': 1.1
    }
}


def transfer_money(amount: decimal.Decimal, sender: UserAccount, reciever: UserAccount, currency: Currency):
    amount_to_deduct = amount * decimal.Decimal(conversion_rates[currency][sender.base_currency])
    amount_to_credit = amount ** decimal.Decimal(conversion_rates[currency][reciever.base_currency])

    if (sender.account_balance < amount_to_deduct):
        raise Exception('Not enough balance')
    sender.account_balance -= amount_to_deduct
    reciever.account_balance += amount_to_credit
    sender.save()
    reciever.save()

    notify(sender, 'Money Deducted', f'You have successfully sent {amount} {currency} to {reciever.full_name}')
    notify(reciever, 'Money Credited', f'{sender.full_name} have sent {amount} {currency}')
    return Transaction.objects.create(
        sender=sender,
        recipient=reciever,
        amount=amount,
        sender_balance=sender.account_balance,
        recipient_balance=reciever.account_balance,
        currency=currency
    )


def send_money_request(amount: decimal.Decimal, sender: UserAccount, reciever: UserAccount, currency: Currency):
    money_request = MoneyRequest.objects.create(
        amount=amount,
        sender=sender,
        recipient=reciever,
        currency=currency,
        status=MoneyRequestStatus.PENDING
    )
    notify(sender, 'Money Request Sent',
           f'You have successfully sent a money request of {amount} {currency} to {reciever.full_name}')
    notify(reciever, 'Money Request Received', f'{sender.full_name} have requested {amount} {currency} from you')
    return money_request


def approve_money_request(request_id: int):
    money_request = MoneyRequest.objects.get(id=request_id)
    if money_request.status == MoneyRequestStatus.PENDING:
        transfer_money(money_request.amount, money_request.recipient, money_request.sender, money_request.currency)
        money_request.status = MoneyRequestStatus.APPROVED
        money_request.save()
    else:
        raise Exception(f'This money request has already been {money_request.status}.')


def deny_money_request(request_id: int):
    money_request = MoneyRequest.objects.get(id=request_id)
    if money_request.status == MoneyRequestStatus.PENDING:
        money_request.status = MoneyRequestStatus.DENIED
        money_request.save()
        notify(money_request.recipient, 'Money Request Denied', f'{money_request.recipient} has denied your money '
                                                                f'request of {money_request.amount} {money_request.currency}')
    else:
        raise Exception(f'This money request has already been {money_request.status}.')
