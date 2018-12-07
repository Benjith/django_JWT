from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from io import BytesIO
from rest_framework.parsers import JSONParser
from django.utils import timezone
import datetime
import psycopg2
import json
import simplejson
import sys
sys.path.append('..')
import polosysBooks
from polosysBooks import models

# Save Chart of Account
@api_view(['POST','GET'])
def saveParty(request):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        # check is customer or vendor
        if data['PartyType'] == 'customer':
            print(data['PartyType'])
            data = BytesIO(request.body)
            data = JSONParser().parse(data)
            chartOfAccData = models.ChartofAccounts()
            # get last inserted id
            latestID = models.ChartofAccounts.objects.last()
            #  is any row 
            if latestID:
                chartOfAccData.AccountID = latestID.AccountID+1
            if not latestID:
                chartOfAccData.AccountID = 1

            chartOfAccData.BranchID = models.Branch.objects.get(BranchID = 1)
            chartOfAccData.AccountCode = data['PartyCode']
            chartOfAccData.AccountName = data['DisplayName']
            chartOfAccData.AccountTypeID = models.AccountType.objects.get(AccountTypeID = 40)
            chartOfAccData.Remarks = 'customer'
            chartOfAccData.isProtected = 0
            chartOfAccData.save()

        elif data['PartyType'] == 'vendor':
            print(data['PartyType'])
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
            chartOfAccData.AccountCode = data['PartyCode']
            chartOfAccData.AccountName = data['DisplayName']
            chartOfAccData.AccountTypeID = models.AccountType.objects.get(AccountTypeID = 22)
            chartOfAccData.Remarks = 'vendor'
            chartOfAccData.isProtected = 0
            chartOfAccData.save()
        latestLedgerId = models.ChartofAccounts.objects.last()
        PartyLedgerID = latestLedgerId.AccountID
        partyData = models.Party()
        lastid = models.Party.objects.last()
        if lastid:
            partyData.PartyID = lastid.PartyID+1
        if not lastid:
            partyData.PartyID = 1001
        partyData.BranchID = models.Branch.objects.get(BranchID = 1)
        partyData.PartyFName = data['PartyFName']
        partyData.PartyLName = data['PartyLName'] 
        partyData.AccountID = models.ChartofAccounts.objects.get(AccountID = PartyLedgerID)
        partyData.PartyCode = data['PartyCode'] 
        partyData.PartyType = data['PartyType'] 
        partyData.DisplayName = data['DisplayName'] 
        partyData.Address = data['Address'] 
        partyData.Email = data['Email']  
        partyData.Mobile = data['Mobile'] 
        partyData.CountryID = models.Country.objects.get(CountryID = data['CountryID'])
        partyData.City = data['City'] 
        partyData.Phone = data['Phone'] 
        partyData.Fax = data['Fax'] 
        partyData.StateID = models.State.objects.get(StateID = data['StateID'])
        partyData.PinCode = data['PinCode'] 
        partyData.GSTRegistrationTypeID = models.GSTRegistrationType.objects.get(GSTRegistrationTypeID = data['GSTRegistrationTypeID'])
        partyData.GSTIN = data['GSTIN'] 
        partyData.TaxNo = data['TaxNo'] 
        partyData.PANNo = data['PANNo'] 
        partyData.OpeningBalance = data['OpeningBalance'] 
        partyData.OpeningDate = data['OpeningDate'] 
        partyData.Remarks = data['Remarks']
        partyData.save()
        responseObj = {"type":"success","message": str(data['DisplayName'])+" Party saved successfully..!"}
    except(ValueError):
        responseObj = {"type":"error","message": "error occur..!"}
    return HttpResponse(json.dumps(responseObj))

# Fetch All Party For Grid View
@api_view(['GET'])
def fetchAllPartyForGridView(request):
    conn = psycopg2.connect(host="localhost",database="polosysbookdb1001", user="postgres", password="root")
    cur = conn.cursor() # books_party."PartyID" books_party."PartyCode" books_party."Email" books_party."Phone" books_party."Mobile" books_party."OpeningBalance"
    cur.execute(""" SELECT books_party."PartyID", books_party."PartyCode", books_party."Email", books_party."Phone", books_party."Mobile", books_party."OpeningBalance", books_party."DisplayName",books_party."PartyCode", books_gstregistrationtype."GSTRegistrationTypeName" FROM public.books_party JOIN public.books_gstregistrationtype ON books_party."GSTRegistrationTypeID_id" = books_gstregistrationtype."GSTRegistrationTypeID"  """)
    row_headers=[x[0] for x in cur.description]
    row = cur.fetchall()
    result_data=[]
    for result in row:
        result_data.append(dict(zip(row_headers,result)))
    return HttpResponse(json.dumps(result_data, default=str))
    
@api_view(['GET'])
def fetchAllPartiesByType(request,partyType):
    try:
        fetchAllData = list(models.Party.objects.filter(PartyType = partyType).values('PartyID', 'DisplayName','AccountID','Email', 'Address'))
        responseData = fetchAllData
    except(ValueError):
        responseData = {"Error Occur..!"}
    return HttpResponse(json.dumps(responseData, default=str))


# Party last code
@api_view(['POST','GET'])
def partyLastCode(request, PartyType):
    try:
        conn = psycopg2.connect(host="localhost",database="polosysbookdb1001", user="postgres", password="root")
        query = """ SELECT MAX("PartyCode") FROM books_party WHERE "PartyType"='"""+PartyType+"""'"""
        cur = conn.cursor()
        print(query)
        cur.execute(query)
        row = cur.fetchall()
        return HttpResponse(json.dumps(row[0][0]))
    except(ValueError) as er:
        return HttpResponse("Error Occur...!"+str(er))

# DELETE CONTACT
@api_view(['GET'])
def deleteParty(request,party_id):
    try:

        accounts = models.Party.objects.values('AccountID').get(PartyID = party_id)
        print(accounts['AccountID'])
        models.Party.objects.get(PartyID=party_id).delete()
        models.ChartofAccounts.objects.get(AccountID = accounts['AccountID'], isProtected = False).delete()
        # 
        responseOBJ = {"message": "Delete successfully....!", "type":"success"}
    except(ValueError):
        responseOBJ = {"type":"error","message":"Error occur in deletion...!"}
    return HttpResponse(json.dumps(responseOBJ))

# EDIT CONTACT
@api_view(['GET'])
def partyDetailsByAccID(request,accoutid):
    try:
        fetchPartyDetailsByAccountID = list(models.Party.objects.filter(AccountID = accoutid).values())    
        return HttpResponse(json.dumps(fetchPartyDetailsByAccountID, default=str))
    except(ValueError):
        return HttpResponse("Error occur")

# EDIT CONTACT
@api_view(['GET'])
def editParty(request,partyid):
    try:
        fetchPartyDetailsByID = list(models.Party.objects.filter(PartyID = partyid).values())    
        return HttpResponse(json.dumps(fetchPartyDetailsByID, default=str))
    except(ValueError):
        return HttpResponse("Error occur")
# Update Party
@api_view(['POST','GET'])
def updateParty(request,partyid):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        partyAcc = models.Party.objects.filter(PartyID = partyid).values()
        AccountID = partyAcc[0]['AccountID_id']
        partyData = models.Party.objects.get(PartyID = partyid)

        chartOfAccData = models.ChartofAccounts.objects.get(AccountID = AccountID)
        if data['PartyType'] == 'customer':
            print(data['PartyType'])

            
            chartOfAccData.AccountCode = data['PartyCode']
            chartOfAccData.AccountName = data['DisplayName']
            chartOfAccData.AccountTypeID = models.AccountType.objects.get(AccountTypeID = 40)
            chartOfAccData.Remarks = 'customer'
            chartOfAccData.isProtected = 0
            chartOfAccData.save()

        elif data['PartyType'] == 'vendor':

            chartOfAccData.AccountCode = data['PartyCode']
            chartOfAccData.AccountName = data['DisplayName']
            chartOfAccData.AccountTypeID = models.AccountType.objects.get(AccountTypeID = 22)
            chartOfAccData.Remarks = 'vendor'
            chartOfAccData.isProtected = 0
            chartOfAccData.save()
            
        
        partyData.BranchID = models.Branch.objects.get(BranchID = 1)
        partyData.PartyFName = data['PartyFName']
        partyData.PartyLName = data['PartyLName'] 
        partyData.PartyCode = data['PartyCode'] 
        partyData.PartyType = data['PartyType'] 
        partyData.DisplayName = data['DisplayName'] 
        partyData.Address = data['Address'] 
        partyData.Email = data['Email']  
        partyData.Mobile = data['Mobile'] 
        partyData.CountryID = models.Country.objects.get(CountryID = data['CountryID'])
        partyData.City = data['City'] 
        partyData.Phone = data['Phone'] 
        partyData.Fax = data['Fax'] 
        partyData.StateID = models.State.objects.get(StateID = data['StateID'])
        partyData.PinCode = data['PinCode'] 
        partyData.GSTRegistrationTypeID = models.GSTRegistrationType.objects.get(GSTRegistrationTypeID = data['GSTRegistrationTypeID'])
        partyData.GSTIN = data['GSTIN'] 
        partyData.TaxNo = data['TaxNo'] 
        partyData.PANNo = data['PANNo'] 
        partyData.OpeningBalance = data['OpeningBalance'] 
        partyData.OpeningDate = data['OpeningDate'] 
        partyData.Remarks = data['Remarks']
        partyData.save()
        responseObj = {"type":"success","message": str(data['DisplayName'])+" Party updated successfully..!"}
    except(ValueError):
        responseObj = {"type":"error","message": "error occur..!"}
    return HttpResponse(json.dumps(responseObj))
