from msilib.schema import Class
import django_filters
from .models import Transaction

class TransactionFilter (django_filters.FilterSet):
    class Meta:
        model=Transaction
        fields=['transaction_type']
