from ninja import Router
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from appV1.schemas import LoginSchemas, Initialisation, EcolbetIdSchemas, TokenSchemas
from appV1.utils import create_token
from ninja.errors import HttpError
import random

from appV1.pay import paymentMethod, checkPaymentT, checkPaymentToken


router = Router()


@router.post('login', tags=['LOGIN ROUTER'], auth=None)
def login(request, data: LoginSchemas):
    username = data.username
    mdp = data.motPasse
    u = User.objects.filter(username=username).exists()
    if u:
        user = authenticate(request, username=username, password=mdp)
        if user is not None:
            # User is authenticated, generate the JWT token
            token = create_token(user.id)
        return {"token": token}
    else:
        raise HttpError(status_code=404, message="User not found")


random_numbers = str(random.randint(0, 99994)).zfill(4) + \
    str(random.randint(0, 99994)).zfill(4)


@router.post('initial/pay', tags=['INITIALISATION PAYMENT ROUTER'])
def initial(request, data: Initialisation):
    try:
        transaction_id = random_numbers
        p = paymentMethod(transaction_id=transaction_id, amount=data.amount, description=data.description,
                          customer_name=data.customer_name, customer_surname=data.customer_surname, customer_phone_number=data.customer_phone_number)
        code = p['code']
        description = p['description']
        message = p['message']
        payment_token = p['data']['payment_token']
        payment_url = p['data']['payment_url']
        print(p)
        return {'status': code, 'description': description, 'response': message, 'url': payment_url, 'token': payment_token, 'ecolbet_id': transaction_id}
    except:
        raise HttpError(status_code=404, message="Ressource not found")


@router.post('check/ecolbet/id', tags=['CHECK TRANSACTION WITCH *ecolbet_id* ROUTER'])
def check(request, t: EcolbetIdSchemas):
    try:
        c = checkPaymentT(t.transcactionId)
        code = c['code']
        message = c['message']
        amount = c['data']['amount']
        currency = c['data']['currency']
        status = c['data']['status']
        payment_method = c['data']['payment_method']
        description = c['data']['description']
        payment_date = c['data']['payment_date']
        return {'status': 200, 'response': message, 'amount': amount, 'currency': currency, 'status': status, 'payment_method': payment_method, 'description': description, 'payment_date': payment_date}
    except:
        raise HttpError(status_code=404, message='ecolbet_id not found')


@router.post('check/token', tags=['CHECK TRANSACTION WITCH *token* ROUTER'])
def check_TOKEN(request, token: TokenSchemas):
    try:
        token = checkPaymentToken(token.token)
        code = token['code']
        message = token['message']
        amount = token['data']['amount']
        currency = token['data']['currency']
        status = token['data']['status']
        payment_method = token['data']['payment_method']
        description = token['data']['description']
        payment_date = token['data']['payment_date']
        return {'status': 200, 'response': message, 'amount': amount, 'currency': currency, 'status': status, 'payment_method': payment_method, 'description': description, 'payment_date': payment_date}
    except:
        raise HttpError(status_code=404, message='token not found')