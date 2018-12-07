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
from django.db import transaction


# get current date and time
currentDate = datetime.datetime.now()

# Save Invetory transaction master
@api_view(['POST','GET'])
def saveAccTransaction(request):
    try:
        with transaction.atomic():
            #AccTransaction Master data 
            data = BytesIO(request.body)
            data = JSONParser().parse(data)            
            for accMaster in data['AccMaster']:    
                accTransactionMasterData = models.AccTransactionMaster()
                latestAccTransaction = models.AccTransactionMaster.objects.last()
                if latestAccTransaction:
                    accTransactionMasterData.AccTransactionMasterID = latestAccTransaction.AccTransactionMasterID+1
                elif not latestAccTransaction:
                    accTransactionMasterData.AccTransactionMasterID = 1
                accTransactionMasterData.BranchID = models.Branch.objects.get(BranchID = accMaster['BranchID'])
                accTransactionMasterData.FinancialYearID =  models.FinancialYears.objects.get(FinancialYearID = accMaster['FinancialYearID'])
                accTransactionMasterData.EmployeeID = models.Employees.objects.get(EmployeeID = accMaster['EmployeeID'])
                # accTransactionMasterData.InvTransactionMasterID =  0
                accTransactionMasterData.InvTransactionMasterID =  models.InvTransactionMaster.objects.get(InvTransactionMasterID = 1)
                accTransactionMasterData.Particulars =  accMaster['AccountName']
                accTransactionMasterData.ActionStatus = accMaster['ActionStatus']
                accTransactionMasterData.TransactionDate = accMaster['TransactionDate']
                accTransactionMasterData.SystemDate = currentDate
                accTransactionMasterData.BankDate = accMaster['TransactionDate']
                accTransactionMasterData.VoucherPrefix = accMaster['VoucherPrefix']
                accTransactionMasterData.VoucherNumber = accMaster['VoucherNumber']
                accTransactionMasterData.VoucherType  = accMaster['VoucherType']
                accTransactionMasterData.VoucherForm   =  accMaster['VoucherForm']
                accTransactionMasterData.ReferenceNumber = accMaster['ReferenceNo']
                accTransactionMasterData.ReferenceDate = accMaster['ReferenceDate']
                accTransactionMasterData.DueDate  = accMaster['DueDate']
                accTransactionMasterData.PaymentMethord  = accMaster['PaymentMethord']
                
                if accTransactionMasterData.VoucherType == 'PI' or accTransactionMasterData.VoucherType == 'PE' or accTransactionMasterData.VoucherType == 'SR':
                    accTransactionMasterData.TotalDebit  = 0
                    accTransactionMasterData.TotalCredit  = accMaster['TotalAmount']
                elif accTransactionMasterData.VoucherType == "SI" or accTransactionMasterData.VoucherType == 'SE' or accTransactionMasterData.VoucherType == 'PR' :
                    accTransactionMasterData.TotalDebit  =  accMaster['TotalAmount']
                    accTransactionMasterData.TotalCredit  = 0
                    
                accTransactionMasterData.TotDiscount  = accMaster['TotDiscount']
                accTransactionMasterData.CommonNarration  = accMaster['CommonNarration']
                accTransactionMasterData.OldAccTransactionMasterID  =  accMaster['OldAccTransactionMasterID']
                accTransactionMasterData.IsInvoicePayment  = accMaster['IsInvoicePayment']
                accTransactionMasterData.IsActive  = accMaster['IsActive']
                accTransactionMasterData.CreatedUserID  = models.Users.objects.get(UserID = accMaster['UserID'])
                accTransactionMasterData.CreatedDate  = currentDate
                accTransactionMasterData.ModifiedUserID  = models.Users.objects.get(UserID = accMaster['UserID'])
                accTransactionMasterData.ModifiedDate  = currentDate
                accTransactionMasterData.save()
                latestAccTransactionID = accTransactionMasterData.AccTransactionMasterID 

               #InvTransaction Deatails data 
            for accDetails in data['AccDetails']:    
                            
                #ACCOUNT DEBICTING   
                accTransactionDetailsData = models.AccTransactionDetails()
                latestAccTransactionDetail = models.AccTransactionDetails.objects.last()
                if latestAccTransactionDetail:
                    accTransactionDetailsData.AccTransactionDetailID = latestAccTransactionDetail.AccTransactionDetailID+1
                elif not latestAccTransactionDetail:
                    accTransactionDetailsData.AccTransactionDetailID = 1
                accTransactionDetailsData.BranchID = models.Branch.objects.get(BranchID = accDetails['BranchID'])
                accTransactionDetailsData.AccTransactionMasterID =  models.AccTransactionMaster.objects.get(AccTransactionMasterID =latestAccTransactionID)
                accTransactionDetailsData.AccountID = models.ChartofAccounts.objects.get(AccountID = accDetails['RelatedAccountID'])
                accTransactionDetailsData.RelatedAccountID = models.ChartofAccounts.objects.get(AccountID = accDetails['AccountID'])
                accTransactionDetailsData.Debit = 0
                accTransactionDetailsData.Credit = accDetails['Amount']
                accTransactionDetailsData.IsDisplay = 1
                accTransactionDetailsData.Discount = accDetails['Discount']
                accTransactionDetailsData.Narration = accDetails['Narration']
                accTransactionDetailsData.save() 
                
                #ACCOUNT CREDITTING
                latestAccTransactionDetailNew = models.AccTransactionDetails.objects.last()
                accTransactionDetailsData.AccTransactionDetailID = latestAccTransactionDetailNew.AccTransactionDetailID+1
                accTransactionDetailsData.BranchID = models.Branch.objects.get(BranchID = accDetails['BranchID'])
                accTransactionDetailsData.AccTransactionMasterID = models.AccTransactionMaster.objects.get(AccTransactionMasterID =latestAccTransactionID)
                accTransactionDetailsData.AccountID = models.ChartofAccounts.objects.get(AccountID = accDetails['AccountID'])
                accTransactionDetailsData.RelatedAccountID = models.ChartofAccounts.objects.get(AccountID = accDetails['RelatedAccountID'])
                accTransactionDetailsData.Debit = accDetails['Amount']
                accTransactionDetailsData.Credit = 0
                accTransactionDetailsData.IsDisplay = 0
                accTransactionDetailsData.Discount = accDetails['Discount']
                accTransactionDetailsData.Narration = accDetails['Narration']
                accTransactionDetailsData.save()   
     
        return HttpResponse(json.dumps(accTransactionDetailsData.AccTransactionDetailID))
        # return HttpResponse("Done")
    except(ValueError) as err:
        return HttpResponse(err)