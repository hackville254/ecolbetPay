from cinetpay_sdk.s_d_k import Cinetpay

apikey = "3968751536516d7e5959d19.88009278"
site_id = "205275"
client = Cinetpay(apikey, site_id)


def paymentMethod(transaction_id, amount, description, customer_name, customer_surname, customer_phone_number):
    data = {
        'amount': amount,
        'currency': "XAF",
        'transaction_id': transaction_id,
        'description': description,
        'return_url': "https://www.exemple.com/return",
        'notify_url': "https://www.exemple.com/notify",
        'customer_name': customer_name,
        'customer_surname': customer_surname,
        'customer_phone_number': customer_phone_number,
    }
    p = client.PaymentInitialization(data)

    print(transaction_id)
    return p


def checkPaymentT(transaction_id):
    c = client.TransactionVerfication_trx(transaction_id)
    print(c)
    return c


def checkPaymentToken(token):
    t = client.TransactionVerfication_token(token)
    print('token----------------------')
    print(t)
    return t
