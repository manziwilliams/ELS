from django.db import models
from twilio.rest import Client

def save(token):
        account_sid ='AC12da270d48af623b306b62f8d6bf7a06'
        auth_token = 'ebfcc9d1c3fe06d31d7037e3124b7bd6'
        client = Client(account_sid, auth_token)
        print("oky" )
        meter_T=str(token)
        message = client.messages.create(
                                    body='Dear customer '' \n Thank you for buying with us , Your token is '+ meter_T +'.',
                                    from_='+13344633671',
                                    to='+250780542954'
                                )

        print(message.sid)

def paymentSMS(token):
        account_sid ='AC12da270d48af623b306b62f8d6bf7a06'
        auth_token = 'ebfcc9d1c3fe06d31d7037e3124b7bd6'
        client = Client(account_sid, auth_token)
        print("oky" )
        meter_T=str(token)
        message = client.messages.create(
                                    body='Dear customer '' \n Your payment was successfully. Thank you.',
                                    from_='+13344633671',
                                    to='+250780542954'
                                )

        print(message.sid)

