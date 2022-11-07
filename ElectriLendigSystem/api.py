from django.db.models import Q
from pickle import GET
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer , TransactionSerializer ,TestSerializer, UnitsSerializer
from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponse
from . import models
from .models import Customers, Transaction, UntisTable,test
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from ElectriLendigSystem import serializers

def save_customer(request):

    if request.method == "POST":
        name=request.POST['name']
        meter=request.POST['meter']
        address=request.POST['address']
        phone=request.POST['contact']
        customer= models.Customers.objects.create(
            meter_number=meter, customer_name=name, customer_phone=phone, customer_address=address)
        CustomerUnits=models.UntisTable.objects.create(
            meter_number=meter,units='0.00'
        )   
        messages.success(request, 'Customer has been created successfully.')
    return redirect('/create_customer')

def getByMeter(request,meter):
    meter = request.POST['meter']
    print(meter)
    customer = models.Transaction.objects.get(meter_number=meter)
    Context={'customer':customer}
    return Context


class CustomerAPI(APIView):

    # 1. List all
    def get(self, request, *arg, **kwargs):
        customers = Customers.objects.filter(user=request.user.id)
        serializer = TransactionSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getborrowingdata(request):
    customers = Transaction.objects.all()
    serializer = TransactionSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getbuyingdata(request):
    customers = Transaction.objects.all()
    serializer = TransactionSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getcustomerdata(request):
    customer = Customers.objects.all()
    serializer = CustomerSerializer(customer, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def testing(request):
    tests = test.objects.all()
    serializer = TestSerializer(tests, many=True)
    return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getcustomerMeterNo(request, meter):
    if meter:
        customer= Customers.objects.get(meter_number=meter)
        serializer= CustomerSerializer(customer)
        return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status":"Not found","data": serializer.errors}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getunits(request, meter):
    if meter:
        units= UntisTable.objects.get(meter_number=meter)
        serializer= UnitsSerializer(units)
        return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status":"Not found","data": serializer.errors}, status=status.HTTP_204_NO_CONTENT) 

@api_view(['GET'])
def testingme(request):
    
        customers= Transaction.objects.filter(Q(transaction_type='BORROW')& Q(is_paid="1"))
        print(customers)
        serializer= TransactionSerializer(customers)
        return Response({"status":"success","data":serializer.data}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def getUnit(request,token):
    if token:
        customer= Transaction.objects.filter(Metertoken=token, is_paid='0').first()
        serializer= TransactionSerializer(customer)
        return Response({"status":"success","data": customer.units}, status=status.HTTP_200_OK)
    else:
        return Response({"status":"Not found","data": serializer.errors}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def postCustomer(request):
    serializer=CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status":"error","data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getBorrowingUnit(request,token):
    if token:
        customerBorrowing = Transaction.objects.filter(Metertoken=token).values()  
        print(customerBorrowing)
        print("we are here!!")
        serializer = TransactionSerializer(customerBorrowing, many=True)
        return Response({"status":"success","data": customerBorrowing.units}, status=status.HTTP_200_OK)
    else:
        return Response({"status":"error","data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def getBuyingUnit(request,token):
    if token:
        customerBuying = Transaction.objects.get(Metertoken=token)
        print(customerBuying)
        serializer = TransactionSerializer(customerBuying, many=True)
        return Response({"status":"success","data": customerBuying.units}, status=status.HTTP_200_OK)
    else:
        return Response({"status":"error","data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class customerView(APIView):

    def post(self,request):
        serializer=CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status":"error","data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,meter=None):
        print("here")
        if meter:
            customer= Customers.objects.get(meter_number=meter)
            serializer= CustomerSerializer(customer)
            return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)

        customers = Customers.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




def RemainingUnits(request):
    if request.method=="POST":
        meter=request.POST['meter']
        print(meter)
        customer=Customers.objects.get(meter_number=meter)
        print(customer.meter_number)
        meter_no=customer.meter_number
        print(meter_no)
        customerBorrowing = Transaction.objects.filter(customer_id=meter_no,is_paid='0').values()
        customersBuying = UntisTable.objects.filter(meter_number=meter).values()
        customersBuying1 = Transaction.objects.all()
        print(customersBuying1)
        print(Transaction)
        # total_units=sum(customersBuying1.values_list('units', flat=True))
        # print(total_units)
        for cust in customersBuying:
            print("oky")
        print("Byemeye")
        return render(request, 'remainingUnits.html',{'CustomersBorrowing':customerBorrowing,'CustomersBuying':customersBuying})
    print("Skipped")
    return render(request, 'check_balance.html')


@api_view(['GET'])
def EnterToken(request,token):
    if token:
        customerBuying = Transaction.objects.filter(Metertoken=token).values()
        
        print(customerBuying)
        serializer = TransactionSerializer(customerBuying, many=True)
        return Response({"status":"success","data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status":"error","data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def test(self, request ,id=None):
#     print("here")
#     if id:
#         customer= Customers.objects.get(id=id)
#         serializer= CustomerSerializer(customer)
#         return Response({"status":"success","data": customer.meter_number}, status=status.HTTP_200_OK)
        
#     customers = Customers.objects.all()
#     serializer = CustomerSerializer(customers, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)