from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from io import BytesIO
from rest_framework.parsers import JSONParser
from django.utils import timezone
import datetime
import psycopg2
import json
import sys
sys.path.append('..')
import polosysBooks
from polosysBooks import models

# Save Chart of Account
@api_view(['POST','GET'])
def saveChartOfAcc(request):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        chartOfAccData = models.ChartofAccounts()
        # get last inserted id
        latestID = models.ChartofAccounts.objects.last()
        #  is any row 
        if latestID:
            chartOfAccData.AccountID = latestID.AccountID+1
        if not latestID:
            chartOfAccData.AccountID = 1001

        chartOfAccData.BranchID = models.Branch.objects.get(BranchID = 1)
        chartOfAccData.AccountCode = data['AccountCode']
        chartOfAccData.AccountName = data['AccountName']
        chartOfAccData.AccountTypeID = models.AccountType.objects.get(AccountTypeID = data['AccountTypeID'])
        chartOfAccData.Remarks = data['Remarks']
        chartOfAccData.isProtected = 0
        chartOfAccData.save()

        responseOBJ = {"type":"success","message":"Cahrt of account saved succefully"}
    except(ValueError) as er:
        responseOBJ = {"type":"error","message":"error occur....!"}
    return HttpResponse(json.dumps(responseOBJ))


# Fetch all chart of account
@api_view(['GET'])
def fetchAllChartOfAccount(request):
    try:
        fetchAllchartOfAccData = list(models.ChartofAccounts.objects.values())
        return HttpResponse(json.dumps(fetchAllchartOfAccData))
    except(ValueError) as er:
        return HttpResponse("Error Occur...!")

@api_view(['GET'])
def fetchAllChartOfAccountForGrid(request):
    conn = psycopg2.connect(host="localhost",database="polosysbookdb1000", user="postgres", password="root")
    cur = conn.cursor() # books_party."PartyID" books_party."PartyCode" books_party."Email" books_party."Phone" books_party."Mobile" books_party."OpeningBalance"
    cur.execute(""" SELECT books_chartofaccounts."AccountID", books_chartofaccounts."AccountCode", books_chartofaccounts."AccountName", books_accounttype."AccountTypeName" FROM public.books_chartofaccounts JOIN public.books_accounttype ON books_chartofaccounts."AccountTypeID_id" = books_accounttype."AccountTypeID";  """)
    row_headers=[x[0] for x in cur.description]
    row = cur.fetchall()
    result_data=[]
    for result in row:
        result_data.append(dict(zip(row_headers,result)))
    return HttpResponse(json.dumps(result_data, default=str))
    

@api_view(['GET'])
def deleteChartOfAccount(request,accountID):
    try:
        is_protected = models.ChartofAccounts.objects.get(AccountID=accountID)
        account_type_id = models.ChartofAccounts.objects.values('AccountTypeID').get(AccountID=accountID)
        accTypeID = account_type_id['AccountTypeID']
        if is_protected.isProtected == True:
            responseOBJ = {"message": str(is_protected.AccountName)+"is protected cannot delete....!", "type":"warning"}

        elif accTypeID == 40:
            responseOBJ = {"message": "Account Receivable is cannot delete....!", "type":"warning"}
        elif accTypeID == 22:   
            responseOBJ = {"message": "Account Payable is cannot delete....!", "type":"warning"}

        elif is_protected.isProtected == False and accTypeID != 40 or accTypeID != 22: 
                models.ChartofAccounts.objects.get(AccountID=accountID,isProtected = False).delete()
                responseOBJ = {"message": str(is_protected.AccountTypeID)+"Delete successfully....!", "type":"success"}
    except ValueError :
        return Response({"message":" error Occur....!", "type":"error"})
    return Response(responseOBJ)

# Edit Details

# EDIT CONTACT
@api_view(['GET'])
def editDetails(request,id):
    try:
        is_protected = models.ChartofAccounts.objects.get(AccountID=id)
        account_type_id = models.ChartofAccounts.objects.values('AccountTypeID').get(AccountID=accountID)
        accTypeID = account_type_id['AccountTypeID']
        if is_protected.isProtected == True:
            responseOBJ = {"message": str(is_protected.AccountName)+"   is protected....!", "type":"warning"}
            return HttpResponse(json.dumps(responseOBJ))

        elif accTypeID == 40:
            responseOBJ = {"message": "Account Receivable is cannot edit....!", "type":"warning"}

        elif accTypeID == 22:   
            responseOBJ = {"message": "Account Payable is cannot edit....!", "type":"warning"}

        elif is_protected.isProtected == False and accTypeID != 40 or accTypeID != 22:
            fetchEditDetailsByID = list(models.ChartofAccounts.objects.filter(AccountID = id).values())    
            return HttpResponse(json.dumps(fetchEditDetailsByID, default=str))
    except(ValueError):
        return HttpResponse("Error occur")

# EDIT CONTACT
@api_view(['GET'])
def accLedgerDetailsForEdit(request,id):
    try:
        is_protected = models.ChartofAccounts.objects.get(AccountID=id)
        account_type_id = models.ChartofAccounts.objects.values('AccountTypeID').get(AccountID=id)
        accTypeID = account_type_id['AccountTypeID']
        if is_protected.isProtected == True:
            responseOBJ = {"message": str(is_protected.AccountName)+"   is protected....!", "type":"warning"}
            return HttpResponse(json.dumps(responseOBJ))

        elif accTypeID == 40:
            responseOBJ = {"message": "Account Receivable is cannot edit....!", "type":"warning"}

        elif accTypeID == 22:   
            responseOBJ = {"message": "Account Payable is cannot edit....!", "type":"warning"}

        elif is_protected.isProtected == False and accTypeID != 40 or accTypeID != 22:
            fetchAccLedgerDetailsByID = list(models.ChartofAccounts.objects.filter(AccountID = id).values())    
            responseOBJ = fetchAccLedgerDetailsByID
            
    except(ValueError):
        responseOBJ = {"message":" error Occur....!", "type":"error"}
    return HttpResponse(json.dumps(responseOBJ, default=str))
    

@api_view(['POST'])
def updateChartOfAccount(request,id):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)

        chartOfAccData = models.ChartofAccounts() 
        chartOfAccData.AccountID = id  
        chartOfAccData.BranchID = models.Branch.objects.get(BranchID = data['BranchID'])
        chartOfAccData.AccountCode = data['AccountCode']
        chartOfAccData.AccountName = data['AccountName']
        chartOfAccData.AccountTypeID = models.AccountType.objects.get(AccountTypeID = data['AccountTypeID'])
        chartOfAccData.Remarks = data['Remarks']
        chartOfAccData.isProtected = 0
        chartOfAccData.save()
        responseObj = {"type":"success","message": str(data['AccountName'])+" Party updated successfully..!"}
    except(ValueError):
        responseObj = {"type":"error","message": "error occur..!"}
    return HttpResponse(json.dumps(responseObj))