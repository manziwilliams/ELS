from django.urls import path, include
from . import views,api
from .api import CustomerAPI, customerView

urlpatterns = [
    path('', views.home_view),
    path('signin/', views.admin_login),
    path('create_customer/', views.create_customer,name='customer-creation'),
    path('admin_dash/', views.admin_dashboard),
    path('customer_table/', views.customer_table),
    path('loan_table/', views.loan_table),  
    path('buy_electricity/', views.buy_electricity),
    path('pay_loan/', views.pay_loan),
    path('borrow_electricity/', views.borrow_electricity),
    path('save_customer/', api.save_customer,name='save-customer'),
    path('check_balance/', views.check_balance), 
    path('show/<int:meter>',views.show),
    path('lend',views.borrow,name='borrowing'),
    path ('buy', views.buying),
    path ('buySMS', views.buySMS),
    path('login', views.loginPage),
    path('logout',views.logoutUser,name='logout'),
    path('sendEmail/', views.sendEmail ),
    path('sending/',views.sending),
    path('success/',views.success),
    path('showLoan/',views.show_loan , name='show-loan'),
    path('pay/',views.PayLoan),
    path('payment/',views.pay),
    path('print/',views.printme),
    path('exportCustomer',views.exportCustomer_scv, name='export-customer'),
    path('exportLoan',views.exportLoan_scv, name='export-loan'),
    path('pdf',views.getpdf,name='pdf'),

    ######################## APIs #################

    path('api/getborrowingdata/',api.getborrowingdata),
    path('api/getbuyingdata/',api.getbuyingdata),
    path('api/getbuyingdata/<int:token>',api.getBuyingUnit),
    path('api/getbuyingdata/<int:token>',api.getUnit),
    path('api/getcustomerMeter/<int:meter>',api.getcustomerMeterNo),
    path('api/customer/',api.getcustomerdata),
    path('api/customerMeter/<int:meter>',customerView.as_view()),
    path('api/test/<int:id>',api.test),
    path('api/testing/',api.testing),
    path('api/testingme/',api.testingme),
    path('remaingunits',api.RemainingUnits, name='remaing-units'),
    path('api/getunit/<int:meter>',api.getunits)

]
