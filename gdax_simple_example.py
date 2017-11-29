import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase


API_KEY = 'GET THIS FROM GDAX'
API_SECRET = 'GET THIS FROM GDAX'
API_PASS = 'GET THIS FROM GDAX'


# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

api_url = 'https://api.gdax.com/'
auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

order_id = 'PUT ORDER ID HERE';
#r = requests.delete(api_url + 'orders/' + order_id, auth=auth)
#print r.json()


# Place an order
order = {
    'size': 100,
    'price': 0.048200,
    'type': 'limit',
    'side': 'sell',
    'product_id': 'ETH-BTC',
    'post_only': 'true',
}
#r = requests.post(api_url + 'orders', json=order, auth=auth)
#print r.json()['id']


# View payment methods
#r = requests.get(api_url + 'payment-methods', auth=auth)
#print r.json()


# Place an order request
order = {
    'amount': 9.22,
    'price': 2286.79,
    'type': 'limit',
    'side': 'buy',
    'product_id': 'BTC-USD',
    'post_only': 'true',
}
#r = requests.post(api_url + 'orders', json=order, auth=auth)
#print r.json()['id']


while 1:
    # Get accounts
    r = requests.get(api_url + 'accounts', auth=auth)
    print r.json()
    for balance in r.json():
        print balance['currency'] + ': ' + balance['balance']

    print ' '

    # show all orders open
    r = requests.get(api_url + 'orders', auth=auth)
    for order in r.json():
        print order['id'] + ': ' + order['product_id'] + ' @ ' + order['price'] + ' FILLED: ' + order['filled_size'] + ' OF ' + order['size']
    time.sleep(20)
    print ' '
