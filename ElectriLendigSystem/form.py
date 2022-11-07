from dataclasses import field, fields
from pyexpat import model
from re import I
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ElectriLendigSystem.models import Customers, CustomersBorrowing ,CustomersBuying

class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customers
        fields="__all__"

class BorrowingForm(forms.ModelForm):
    class Meta:
        model=CustomersBorrowing
        fields="__all__"

class Buyingform(forms.ModelForm):
    class Meta:
        model=CustomersBuying
        fields="__all__"

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields ="__all__"


