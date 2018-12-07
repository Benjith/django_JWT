from django.http import HttpResponse
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from io import BytesIO
from rest_framework.parsers import JSONParser
import json
import sys
sys.path.append('..')
import polosysBooks
from polosysBooks import models
from django.db import transaction

#insert
@api_view(['POST'])
def saveEmployee(request):
    with transaction.atomic():
        try:
            print("HAi") 
            data = BytesIO(request.body)
            data = JSONParser().parse(data)
            # print(data) 
            # print(data['firstName'] + " " + data['middleName'] + " " + data['lastName'])
            # 
            # Insert Ledgers
            chartOfAccData = models.ChartofAccounts()
            latestID = models.ChartofAccounts.objects.last()
            chartOfAccData.AccountID = latestID.AccountID+1
            chartOfAccData.BranchID =  models.Branch.objects.get(BranchID = data['branchID'])         
            chartOfAccData.AccountCode = latestID.AccountID+1 
            chartOfAccData.AccountName = data['firstName'] + " " + data['middleName'] + " " + data['lastName']
            chartOfAccData.AccountTypeID =  models.AccountType.objects.get(AccountTypeID = 18)
            chartOfAccData.Remarks = data['remarks']
            chartOfAccData.save()
            EmployeeLedgerID = chartOfAccData.AccountID
            #Insert Employee
            employee = models.Employees()
            lastid = models.Employees.objects.last()
            print(lastid.EmployeeID)
                
            if lastid is None: 
                employee.EmployeeID = 1
            else:            
                employee.EmployeeID = lastid.EmployeeID + 1 
            employee.BranchID=models.Branch.objects.get(BranchID=data['branchID'])
            employee.EmployeeCode=data['employeeCode']
            employee.Title = data['title']
            employee.FirstName = data['firstName']
            employee.MiddleName=data['middleName']
            employee.LastName=data['lastName']
            employee.DisplayName = data['displayName']
            employee.GenderName = data['genderName']
            employee.DateofBirth=data['dateofBirth']
            employee.Address=data['address']
            employee.Email = data['email']
            employee.Phone = data['phone']
            employee.City=data['city']
            employee.AccountID=models.ChartofAccounts.objects.get(AccountID=EmployeeLedgerID)
            employee.StateID = models.State.objects.get(StateID=data['stateID'])
            employee.HireDate = data['hireDate']
            employee.EmployeeDesignationID = models.EmployeeDesignation.objects.get(EmployeeDesignationID=data['employeeDesignationID'])
            employee.CountryID = models.Country.objects.get(CountryID=data['countryID'])
            employee.PINcode = data['pinCode']
            employee.BillingRate = data['billingRate']
            employee.BillingType = data['billingType'] 
            employee.Remarks = data['remarks'] if 'remarks' in data else ''
            employee.save()
            responseOBJ = {"message":" saved successfully....!", "type":"success"}        
        except ValueError:
            return Response({"Not Saved":" Error in insertion....!", "type":"error"})
        return Response(responseOBJ)
#get    
@api_view(['GET'])
def getEmployee(request):
    try:
        responseOBJ = list(models.Employees.objects.values())
        print(json.dumps(responseOBJ,default=str))
        return HttpResponse(json.dumps(responseOBJ,default=str))
    except ValueError:
        return Response(json.dumps("Sorry, an unknown error happened"))   
#get    
@api_view(['GET'])
def getEmployeeByID(request,employeeID):
    try:
        responseOBJ = list(models.Employees.objects.filter(EmployeeID = employeeID).values())    
        return HttpResponse(json.dumps(responseOBJ,default=str))
    except ValueError:
        return Response(json.dumps("Sorry, an unknown error happened"))           
#delete              
@api_view(['GET'])
def deleteEmployee(request,deletedId):
    try:
        models.Employees.objects.get(EmployeeID=deletedId).delete()
        responseOBJ = {"message":"Delete successfully....!", "type":"success"}
        return Response(responseOBJ)       
    except ValueError:
        return HttpResponse({"message": "Error in delete","type" :"error" })
#update            
@api_view(['POST'])
def updateEmployee(request,updatedId):
    with transaction.atomic():
        try:
            data = BytesIO(request.body)
            data = JSONParser().parse(data)
             # Update Ledger Name
            chartOfAccData = models.ChartofAccounts.objects.get(AccountID=data['accountID'])    
            chartOfAccData.AccountName = data['firstName'] + " " + data['middleName'] + " " + data['lastName']
            chartOfAccData.save()

            # Update Ledger Name
            employee = models.Employees.objects.get(EmployeeID = updatedId)        
            employee.BranchID=models.Branch.objects.get(BranchID=data['branchID'])
            employee.EmployeeCode=data['employeeCode']
            employee.Title = data['title']
            employee.FirstName = data['firstName']
            employee.MiddleName=data['middleName']
            employee.LastName=data['lastName']
            employee.DisplayName = data['displayName']
            employee.GenderName = data['genderName']
            employee.DateofBirth=data['dateofBirth']
            employee.Address=data['address']
            employee.Email = data['email']
            employee.Phone = data['phone']
            employee.City=data['city']
            employee.AccountID=models.ChartofAccounts.objects.get(AccountID=data['accountID'])
            employee.StateID = models.State.objects.get(StateID=data['stateID'])
            employee.HireDate = data['hireDate']
            employee.EmployeeDesignationID = models.EmployeeDesignation.objects.get(EmployeeDesignationID=data['employeeDesignationID'])
            employee.CountryID = models.Country.objects.get(CountryID=data['countryID'])
            employee.PINcode = data['pinCode']
            employee.BillingRate = data['billingRate']
            employee.BillingType = data['billingType']
            employee.Remarks = data['remarks']
            employee.save()
            responseOBJ = {"message":"updated successfully....!", "type":"success"}   
            return Response(responseOBJ)       
        except ValueError:
            return HttpResponse({"message": "Error in updation","type" :"error" })