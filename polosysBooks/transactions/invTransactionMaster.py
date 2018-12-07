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
import datetime

# get current date and time
currentDate = datetime.datetime.now()

# Save Invetory transaction master
@api_view(['POST','GET'])
def saveInvTransactionMaster(request):
    try:
        #  InvTransactionMasterID  BranchID FinancialYearID EmployeeID AccountID VoucherPrefix VoucherNumber VoucherType VoucherForm TransactionDate ActionStatus SystemDate ReferenceNo ReferenceDate ShippingAddress  DueDate DueAmount TotalGross TotalDiscount BillDiscount TotalTax TotalNetValue TotalNetAmount RoundAmount GrandTotal AdvanceAmount CurrencyID ExchangeRate WarehouseID IsInvoiced IsPosted CashAmt CreditAmt BankAmt IsActive CreatedUserID CreatedDate ModifiedUserID ModifiedDate
        data = BytesIO(request.body)
        data = JSONParser().parse(data)

        transactionData = models.InvTransactionMaster()

        latestInvTransaction = models.InvTransactionMaster.objects.last()
        if latestInvTransaction:
            transactionData.InvTransactionMasterID = latestInvTransaction.InvTransactionMasterID+1

        elif not latestInvTransaction:
            transactionData.InvTransactionMasterID = 1001
        # 
        if data['VoucherType'] == 'SE':  
            transactionData.BranchID =  models.Branch.objects.get(BranchID = data['BranchID'])
            transactionData.FinancialYearID =  models.FinancialYears.objects.get(FinancialYearID = 1)
            transactionData.EmployeeID =  models.Employees.objects.get(EmployeeID = 1)
            transactionData.AccountID =  models.ChartofAccounts.objects.get(AccountID = data['AccountID'])
            # transactionData.VoucherPrefix 
            transactionData.VoucherNumber = data['VoucherNumber']
            transactionData.VoucherType = data['VoucherType']
            # transactionData.VoucherForm 
            transactionData.TransactionDate = data['TransactionDate']
            transactionData.ActionStatus = 'A'
            transactionData.SystemDate = currentDate
            if data['ReferenceNo']:
                transactionData.ReferenceNo = data['ReferenceNo']
            
            transactionData.ReferenceDate = data['ReferenceDate']
            transactionData.ShippingAddress  = data['ShippingAddress']
            transactionData.DueDate = data['DueDate']
            transactionData.DueAmount = 0
            transactionData.TotalGross = 1000
            transactionData.TotalDiscount = 0
            transactionData.BillDiscount = 50
            transactionData.TotalTax = 250
            transactionData.TotalNetValue = 1000
            transactionData.TotalNetAmount = 1250
            transactionData.RoundAmount = 0
            transactionData.GrandTotal = transactionData.TotalNetAmount-transactionData.BillDiscount
            transactionData.AdvanceAmount = data['AdvanceAmount']
            transactionData.CurrencyID =  models.Currencies.objects.get(CurrencyID = 1)
            # transactionData.ExchangeRate = data['']
            transactionData.WarehouseID =   models.Warehouse.objects.get(WarehouseID = 1)
            transactionData.IsInvoiced = 0
            transactionData.IsPosted = 0
            transactionData.CashAmt = transactionData.GrandTotal
            transactionData.CreditAmt = data['CreditAmt']
            transactionData.BankAmt = data['BankAmt']
            transactionData.IsActive = 1
            transactionData.CreatedUserID = models.Users.objects.get(UserID = 1)
            transactionData.CreatedDate = currentDate
            transactionData.ModifiedUserID = models.Users.objects.get(UserID = 1)
            transactionData.ModifiedDate = currentDate
            transactionData.save()
            latestInvTransactionID = {"message":"Success","type":"success"}
        else:

            latestInvTransactionID = transactionData.InvTransactionMasterID #test
        return HttpResponse(json.dumps(latestInvTransactionID))
    except(ValueError) as err:
        return HttpResponse(err)
    
    
@api_view(['GET'])
def setLatestVoucharNo(request,voucharType):
    try:
        lastRecordByVoucharType = models.InvTransactionMaster.objects.filter(VoucherType= voucharType)
        if lastRecordByVoucharType:
            conn = psycopg2.connect(host="localhost",database="polosysbookdb1000", user="postgres", password="root")
            query = """ SELECT MAX("VoucherNumber") FROM books_invtransactionmaster WHERE "VoucherType"='"""+voucharType+"""'"""
            cur = conn.cursor()
            print(query)
            cur.execute(query)
            row = cur.fetchall()
            latestVoucherNo = row[0][0]
            return HttpResponse(json.dumps(latestVoucherNo+1))
        elif not lastRecordByVoucharType:
            latestVoucherNo = 1001
            return HttpResponse(json.dumps(latestVoucherNo))
    except(ValueError):
        return HttpResponse("Error Occur....!")
            
    