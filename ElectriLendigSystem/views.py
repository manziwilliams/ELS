from ast import And
import imp
from .filter import TransactionFilter
from asyncio.windows_events import NULL
from audioop import add
from contextvars import Context
from email import header
from django_filters import filters
from lib2to3.pytree import convert
from multiprocessing import context
from pickle import GET, NONE
import random
from . import sms
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from reportlab.pdfgen import canvas  
from urllib import response
from twilio.rest import Client
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect  
from django.shortcuts import redirect, render, HttpResponse
from . import models,sms
from .models import Customers, Transaction
import csv,datetime
from dateutil import parser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required


# Create your views here.

Payment_meter_number=NULL
Meter_token=NULL
token=NULL

def printme(request):
    print(  Payment_meter_number)
    cust=Customers.objects.get(meter_number=Payment_meter_number)
    print("true")
    print(cust.id)
    id=cust.id
    sms.paymentSMS()
    Transaction.objects.filter(customer=id).update(is_paid="1")
    return render(request, "index.html")

def home_view(request):
    return render(request, "index.html")

def success(request):
    return render(request, "thankyou.html")


def admin_login(request):
    return render(request, "signin.html")

def pay(request):
    return render(request, "Pay.html")


def buy_electricity(request):
    return render(request, "buy_electricity.html")

def pay_loan(request):
    return render(request, "pay_loan.html")

def create_customer(request):
    return render(request, "customer_registration.html")


def borrow_electricity(request):
    return render(request, "borrow_electricity.html")


def check_balance(request):
    return render(request, "check_balance.html")


def show(request,meter):
    customer = models.Customers.objects.get(meter_number=meter)
    print(customer)
    return render(request, "show.html", {'customer': customer})

def show_loan(request):
    print("show loan")
    loans=models.Transaction.objects.all()
    myFilter=TransactionFilter(request.GET,queryset=loans)
    # loans=myFilter.qs
    print("Hi")
    print(myFilter.qs)
    return render(request, "loan_table.html", {'myFilter':myFilter})
def listing(request):
    loans=models.Transaction.objects.all()
    myFilter=TransactionFilter(request.GET,queryset=loans)
    loan=myFilter.qs
    print(loans)
    return render(request, "Hello.html", {'loans': loans,'myFilter':myFilter})

def filter(request):
    print("filtering")
    loans=models.Transaction.objects.all()
    myFilter=TransactionFilter(request.GET,queryset=loans)
    loan=myFilter.qs
    print(loans)
    return render(request, "loan_table.html", {'loans': loans,'myFilter':myFilter})
    
def MetertokenNumber(N):
	minimum = pow(10, N-1)
	maximum = pow(10, N) - 1
	return random.randint(minimum, maximum)


def borrow(request):
    
    if request.method == "POST":
        meter = request.POST['meter']
        customer =Customers.objects.filter(meter_number=meter).first()
        if not customer :
            messages.success(request, 'Invalid meter')
            return render(request, 'borrow_electricity.html')
        print(customer.id)
        id=customer.id
        Trans= Transaction.objects.filter( customer=id,is_paid='0',transaction_type='BORROW').first()
        print("True")
        print(customer.id)
        if   Trans:
            messages.success(request, 'First pay , The previous loan')
            return render(request, 'borrow_electricity.html')
        amount = request.POST['amount']
        metertoken=MetertokenNumber(16)
        paymentToken=PaymenttokenNumber()
        dead_line=datetime.datetime.today() + datetime.timedelta(days=15)
        print(dead_line)
        print(metertoken)
        print(paymentToken)
        convert_amount=int(amount)
        inter=interest(convert_amount)
        units=borrowingunits(convert_amount)
        paidbalance=0
        if convert_amount < 1500:
            borrow = models.Transaction.objects.create(
            customer_id=customer.id, amount=amount, units=units,Metertoken=metertoken,transaction_type='BORROW',is_paid=0,PaymentToken=paymentToken,RemaingBalance=amount,PiadBalance=paidbalance , deadline=dead_line,interest=inter)
            UnitsInDB = models.UntisTable.objects.get(meter_number=meter)
            n1=float(UnitsInDB.units)
            n2=float(units)
            updatedUnitsInt= n1 + n2
            updatedUnitsStr=str(updatedUnitsInt)
            print(updatedUnitsInt)
            UnitsUpdate=models.UntisTable.objects.filter(meter_number=meter).update(units=updatedUnitsStr)
            messages.success(request, 'Data has been submitted')
            sms.save(metertoken)
            return render(request, 'thankyou1.html')
        else:
            messages.success(request, 'Units must be below 1500')
            return render(request, 'borrow_electricity.html')
    return render(request, 'borrow_electricity.html')



def PaymenttokenNumber():
    random_number = random.randint(1111111,9999999)
    token=("999"+str(random_number))
    print(int(token))
    return token

def buying(request):
    if request.method == "POST":
        meter = request.POST['meter']
        customer =Customers.objects.filter(meter_number=meter).first()
        if not customer:
            messages.success(request, 'Invalid meter')
            return render(request, 'buy_electricity.html')
        id=customer.id
        Trans= Transaction.objects.filter( customer=id,is_paid='0',transaction_type='BORROW').first()
        print("True")
        if   Trans:
            messages.success(request, 'First pay , The previous loan')
            return render(request, 'buy_electricity.html')
        amount = request.POST['amount']
        convert_units=int(amount)
        units=buyingunits(convert_units)
        metertoken=MetertokenNumber(16)
        paymenttoken=PaymenttokenNumber()
        dead_line=datetime.datetime.today() 
        print(dead_line)        
        global Meter_token

        global token
        paymenttoken=token
        Meter_token=metertoken
        buying= models.Transaction.objects.create(
            customer_id=customer.id, amount=amount, units=units,Metertoken=metertoken,transaction_type='BUY',is_paid=1,PaymentToken=paymenttoken,RemaingBalance=NULL,PiadBalance=NULL,interest=NULL,deadline=dead_line)
        messages.success(request, 'Data has been submitted')
        UnitsInDB = models.UntisTable.objects.get(meter_number=meter)
        n1=float(UnitsInDB.units)
        n2=float(units)
        updatedUnitsInt= n1 + n2
        updatedUnitsStr=str(updatedUnitsInt)
        print(updatedUnitsInt)
        UnitsUpdate=models.UntisTable.objects.filter(meter_number=meter).update(units=updatedUnitsStr)

    return render(request, 'thankyou.html',{'amount':amount})


def buySMS(request):
    sms.save(Meter_token)
    return render(request, "index.html")

def PayLoan(request):
  if request.method == "POST":
        meter = request.POST['meter']
        customer =Customers.objects.filter(meter_number=meter).first()
        if not customer :
            messages.success(request, 'Invalid meter')
            return render(request, 'pay_loan.html')
        print(customer.id)
        id=customer.id
        Trans= Transaction.objects.filter( customer=id,is_paid='0',transaction_type='BORROW').first()
        print("True")
        print(customer.id)
        if   Trans:
            global Payment_meter_number
            Payment_meter_number=meter
            print(Payment_meter_number)
            amou=int(Trans.amount)
            inte=int(float(Trans.interest))
            print(Trans.amount)
            print(Trans.interest)
            totalAmount= amou+inte
            print(totalAmount) 
            messages.success(request, 'you have a loan')
            return render(request, 'pay.html',{'totalAmount': totalAmount,'Trans':Trans})
        else:
            messages.success(request, 'you dont have a loan')
            return render(request, 'pay_loan.html')


def borrowingunits(N):
    units=N/89
    return units

def buyingunits(N):
    if N<1500:
        units=N/89
        return units
    elif N>1500 and N<10500:
        units=N/212
        return units
    else:
        units=N/249
        return units

def interest(N):
    if N<1500:
        units=(N*15)/100
        return units

def loginPage(request):
    
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username)
        print(password)
        user =authenticate(request , username=username , password=password)
        print(user)

        if user is not None:
            login (request, user)
            print("hello")
            return redirect ('/admin_dash')
        else:
            messages.info(request, 'Username OR password is incorrect')  
    
    return render(request, 'signin.html')


def logoutUser(request):
	logout(request)
	return redirect('/login')

@login_required(login_url='/login')
def customer_table(request):
    customers = models.Customers.objects.all()
    return render(request, "customer_table.html", {'customers': customers})

@login_required(login_url='/login')
def loan_table(request):
    return render(request, "loan_table.html")

@login_required(login_url='/login')
def admin_dashboard(request):
    Transaction=models.Transaction.objects.all()
    loans=models.Transaction.objects.filter(transaction_type='BORROW')
    loansNo=models.Transaction.objects.filter(transaction_type='BORROW').count()
    buyingNo=models.Transaction.objects.filter(transaction_type='BUY').count()
    customerNo=models.Customers.objects.count()
    print(loansNo)
    print(customerNo)
    return render(request, "admin_dashboard.html", {'loans': loans ,'loansNo': loansNo,'customerNO':customerNo,'buyingNo':buyingNo,'Transaction':Transaction})



def sendEmail(request):
    print("twinjiyee")
    subject = request.POST.get['subject']
    message = request.POST.get['message']
    from_email = request.POST.get['email']
    print(message)
    print("going to send")
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['admin@example.com'])
            messages.success(request, 'Message sent succefully')
        except :
            return HttpResponse('Invalid header found.')

def sending(request):
    send_mail('Hello from willy',
    'Hello there. This is a message',
    'manziwilliams18@gmail.com',
    ['manziwilliams18@gmail.com'],
    fail_silently=False)

    return render(request,'sentEM.html')


def sendSMS(request):
    account_sid ='AC12da270d48af623b306b62f8d6bf7a06'
    auth_token = 'ebfcc9d1c3fe06d31d7037e3124b7bd6'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                body='Hi there',
                                from_='+13344633671',
                                to='+250780542954'
                            )

    print(message.sid)


def exportCustomer_scv(request):

    response=HttpResponse(content_type='text/csv')  
    response['Content-Disposition']='attachment; filename=Customer-' + \
         str(datetime.date.today()) +'.csv'

    writer =csv.writer(response)
    writer.writerow(['Meter Number','Name','Phone','Address'])

    customers=models.Customers.objects.all()
    for customer in customers:
        writer.writerow([customer.meter_number,customer.customer_name,
                        customer.customer_phone, customer.customer_address])
    
    return response

def exportLoan_scv(request):

    response=HttpResponse(content_type='text/csv')  
    response['Content-Disposition']='attachment; filename=Customers With Loan-' + \
         str(datetime.date.today()) +'.csv'

    writer =csv.writer(response)
    writer.writerow(['Meter Number','Name','Phone','Address','Amount','Unit','Token','Date'])

    customers=Transaction.objects.all()

    for customer in customers:
        writer.writerow([customer.meter_number,customer.customer_name, customer.customer_phone,customer.customer_address,customer.amount,customer.units,customer.token,customer.datetime])

    return response


def getpdf(request):  
    response = HttpResponse(content_type='application/pdf')  
    response['Content-Disposition'] = 'attachment; filename="file.pdf"' 
    customers=Transaction.objects.all() 
    p = canvas.Canvas(response)  
    p.setFont("Times-Roman", 55)  
    p.drawString(100,700, "Hello, Javatpoint.")  
    p.showPage()  
    p.save()  
    return response  


