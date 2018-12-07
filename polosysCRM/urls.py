from django.urls import include, path
from django.conf.urls import url
from .signin.view import authenticate_user 
from .masterDetails import customers

urlpatterns = [   
# Haris

















# Benjith
path('signin/', authenticate_user, name='main-view'),























#Muhsin
 path('saveCustomer/' ,customers.saveCustomer, name='saveCustomerAuth'), 
 path('isEmailAlreadyExist/<str:emailid>/', customers.emailAlreadyExist, name='emailIsValidOrNot')

]





