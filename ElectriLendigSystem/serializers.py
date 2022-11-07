from dataclasses import field
from pyexpat import model
import unittest
from rest_framework import serializers
from .models import Customers,Transaction,test,UntisTable
 
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields ='__all__'

        # fields =["meter_number","customer_name","customer_phone","customer_address"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields ='__all__'



class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model=test
        fields='__all__'

class UnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model=UntisTable
        fields='__all__'

