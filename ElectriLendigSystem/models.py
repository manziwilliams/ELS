from ast import Delete
from datetime import datetime
from pyexpat import model
from select import select
from statistics import mode
from tkinter import CASCADE
from turtle import st
from unittest.util import _MAX_LENGTH
from django.db import models
from twilio.rest import Client
# Create your models here.


class Customers(models.Model):
    meter_number= models.CharField(max_length=16)
    customer_name= models.CharField(max_length=255)
    customer_phone= models.CharField(max_length=13)
    customer_address= models.CharField(max_length=255)
    def __str__(self):
        return self.customer_name
    

class Transaction(models.Model):
    customer =models.ForeignKey(Customers,  on_delete=models.PROTECT)
    transaction_types = (
        ('BUY', 'BUY'),
        ('BORROW', 'BORROW')
    )
    transaction_type = models.CharField(default='BUY',choices=transaction_types, max_length=30 )
    amount=models.CharField(max_length=15)
    interest=models.CharField(max_length=20)
    units=models.CharField(max_length=20)
    Metertoken=models.CharField(max_length=16)
    PaymentToken=models.CharField(max_length=16)
    RemaingBalance=models.CharField(max_length=16)
    PiadBalance=models.CharField(max_length=16)
    datetime=models.DateTimeField(auto_now=True)
    deadline=models.DateField()
    is_paid = models.BooleanField(default=True)

    def __str__(self):
        return str(self.PaymentToken)

    # def save(self, *args, **kwargs):
        account_sid ='AC12da270d48af623b306b62f8d6bf7a06'
        auth_token = 'ebfcc9d1c3fe06d31d7037e3124b7bd6'
        client = Client(account_sid, auth_token)
        print(self.PaymentToken )
        message = client.messages.create(
                                    body='Dear customer '' \n Thank you for buying with us , Payment token is '+ self.PaymentToken +'.',
                                    from_='+13344633671',
                                    to='+250780542954'
                                )

        print(message.sid)
        return super().save(*args,**kwargs)


class PaymentTable(models.Model):
    transaction= models.ForeignKey(Transaction,  on_delete=models.PROTECT)
    amount=models.CharField(max_length=14)
    def __str__(self):
        return self.transaction


class UntisTable(models.Model):
    meter_number= models.CharField(max_length=16)
    units=models.CharField(max_length=14)
    def __str__(self):
        return self.units
    


class Admin(models.Model):
    customer =models.ForeignKey(Customers,  on_delete=models.PROTECT)
    admin_email = models.CharField(max_length=45)
    password= models.CharField(max_length=45)
    def __str__(self):
        return self.admin_email

class test(models.Model):
    customer = models.OneToOneField(Customers , on_delete=models.CASCADE)
    father = models.CharField(max_length=50)

    def __str__(self):
        return self.father

  