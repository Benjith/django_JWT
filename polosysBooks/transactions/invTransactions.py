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
import datetime
import decimal
from django.db.models import Sum, Avg, Min, Max, Count
import psycopg2
# get current date and time
currentDate = datetime.datetime.now()


@api_view(['GET'])
def getMaxVoucherNo(request,voucharType):
    VoucherNo = models.InvTransactionMaster.objects.filter(VoucherType=voucharType,IsActive=True).aggregate(Max('VoucherNumber'))
    print(VoucherNo)
    return HttpResponse(json.dumps(VoucherNo,default=str))
#insert
@api_view(['POST','GET'])
def saveInvTransaction(request):
    try:
        with transaction.atomic():
            #InvTransaction Master data 
            data = BytesIO(request.body)
            data = JSONParser().parse(data)
            print("mASTER AND dETAILS eNTER")
            print(data)            
            for invMaster in data['InvMaster']:
                invTransactionMasterData = models.InvTransactionMaster()

                latestInvTransaction = models.InvTransactionMaster.objects.last()
                if latestInvTransaction:
                    invTransactionMasterData.InvTransactionMasterID = latestInvTransaction.InvTransactionMasterID+1

                elif not latestInvTransaction:
                    invTransactionMasterData.InvTransactionMasterID = 1
                #InvTransaction master data 
                invTransactionMasterData.BranchID =  models.Branch.objects.get(BranchID = invMaster['BranchID'])
                invTransactionMasterData.FinancialYearID =    models.FinancialYears.objects.get(FinancialYearID = invMaster['FinancialYearID'])
                invTransactionMasterData.EmployeeID =  models.Employees.objects.get(EmployeeID = invMaster['EmployeeID'])
                invTransactionMasterData.AccountID =  models.ChartofAccounts.objects.get(AccountID = invMaster['AccountID'])
                invTransactionMasterData.VoucherPrefix = invMaster['VoucherPrefix'] if invMaster['VoucherPrefix'] in data else ''
                invTransactionMasterData.VoucherNumber = invMaster['VoucherNumber']
                invTransactionMasterData.VoucherType = invMaster['VoucherType']
                invTransactionMasterData.VoucherForm = invMaster['VoucherForm'] if 'VoucherForm' in invMaster else ''
                invTransactionMasterData.TransactionDate = invMaster['TransactionDate']                
                invTransactionMasterData.SystemDate =   invMaster['TransactionDate']
                invTransactionMasterData.ReferenceNo = invMaster['ReferenceNo'] if 'ReferenceNo' in invMaster else ''
                print(invTransactionMasterData.ReferenceNo) 
                invTransactionMasterData.ReferenceDate = invMaster['ReferenceDate']
                invTransactionMasterData.ShippingAddress  = invMaster['ShippingAddress'] if 'ShippingAddress' in invMaster else ''
                invTransactionMasterData.DueDate = invMaster['DueDate'] 
                invTransactionMasterData.DueAmount = invMaster['DueAmount']
                invTransactionMasterData.TotalGross = invMaster['TotalGross']
                invTransactionMasterData.TotalDiscount = invMaster['TotalDiscount']
                invTransactionMasterData.BillDiscount = invMaster['BillDiscount']
                invTransactionMasterData.TotalTax = invMaster['TotalTax']
                invTransactionMasterData.TotalNetValue = invMaster['TotalNetValue']
                invTransactionMasterData.TotalNetAmount = invMaster['TotalNetAmount']
                invTransactionMasterData.RoundAmount = invMaster['RoundAmount']
                invTransactionMasterData.GrandTotal = invMaster['GrandTotal']
                invTransactionMasterData.AdvanceAmount = invMaster['AdvanceAmount']
                invTransactionMasterData.CurrencyID =  models.Currencies.objects.get(CurrencyID = invMaster['CurrencyID'])
                invTransactionMasterData.WarehouseID =   models.Warehouse.objects.get(WarehouseID = invMaster['WarehouseID'])
                invTransactionMasterData.IsInvoiced = invMaster['IsInvoiced']
                invTransactionMasterData.IsPosted = invMaster['IsPosted']
                invTransactionMasterData.CashAmt = invMaster['CashAmt']
                invTransactionMasterData.CreditAmt = invMaster['CreditAmt']
                invTransactionMasterData.BankAmt = invMaster['BankAmt']
                invTransactionMasterData.IsActive = invMaster['IsActive']
                invTransactionMasterData.CreatedUserID = models.Users.objects.get(UserID = invMaster['UserID'])
                invTransactionMasterData.ModifiedUserID = models.Users.objects.get(UserID = invMaster['UserID'])                
                invTransactionMasterData.OldInvTransactionID = invMaster['OldInvTransactionID']
                invTransactionMasterData.ActionStatus = "A"
                if invTransactionMasterData.OldInvTransactionID > 0:
                    invTransactionMasterData.CreatedDate =  invMaster['CreatedDate']
                    message =  "Update successfully....!" 
                elif invTransactionMasterData.OldInvTransactionID==0:                   
                    invTransactionMasterData.CreatedDate =  currentDate
                    message =  "Saved successfully....!"
                invTransactionMasterData.ModifiedDate =  currentDate    
                invTransactionMasterData.Remarks =  invMaster['Remarks'] if 'Remarks' in invMaster else '' 
                invTransactionMasterData.ExchangeRate =  invMaster['ExchangeRate'] 
                TotalAmount = invTransactionMasterData.GrandTotal    
                Remarks = invTransactionMasterData.Remarks   
                TotalDiscount =  invTransactionMasterData.TotalDiscount       
                invTransactionMasterData.save()
                latestInvTransactionID = invTransactionMasterData.InvTransactionMasterID 
                print(latestInvTransactionID)

            #InvTransaction Deatails data 
            for invDetails in data['InvDetails']:    
                invTransactionDetailsData = models.InvTransactionDetails()
                latestInvTransactionDetail = models.InvTransactionDetails.objects.last()
                if latestInvTransactionDetail:
                    invTransactionDetailsData.InvTransactionDetailID = latestInvTransactionDetail.InvTransactionDetailID+1
                elif not latestInvTransactionDetail:
                    invTransactionDetailsData.InvTransactionDetailID = 1
                
                invTransactionDetailsData.BranchID = models.Branch.objects.get(BranchID = invMaster['BranchID'])
                invTransactionDetailsData.InvTransactionMasterID = models.InvTransactionMaster.objects.get(InvTransactionMasterID =latestInvTransactionID)
                invTransactionDetailsData.ItemID = models.Items.objects.get(ItemID = invDetails['ItemID'])
                invTransactionDetailsData.UnitID = models.UnitOfMeasures.objects.get(UnitID = invDetails['UnitID'])
                invTransactionDetailsData.Quantity = invDetails['Quantity']
                invTransactionDetailsData.Rate = invDetails['Rate']
                invTransactionDetailsData.RateWithTax = invDetails['RateWithTax']
                invTransactionDetailsData.GrossValue = invDetails['GrossValue']
                invTransactionDetailsData.DiscountPerc = invDetails['DiscountPerc']
                invTransactionDetailsData.DiscountAmt = invDetails['DiscountAmt']
                invTransactionDetailsData.VatPerc = invDetails['VatPerc']
                invTransactionDetailsData.VatAmount = invDetails['VatAmount']
                invTransactionDetailsData.CessPerc = invDetails['CessPerc']
                invTransactionDetailsData.CessAmount = invDetails['CessAmount']
                invTransactionDetailsData.SGSTPerc = invDetails['SGSTPerc']
                invTransactionDetailsData.SGSTAmount = invDetails['SGSTAmount']
                invTransactionDetailsData.CGSTPerc = invDetails['CGSTPerc']
                invTransactionDetailsData.CGSTAmount = invDetails['CGSTAmount']
                invTransactionDetailsData.IGSTPerc = invDetails['IGSTPerc']
                invTransactionDetailsData.IGSTAmount = invDetails['IGSTAmount']
                invTransactionDetailsData.NetValue = invDetails['NetValue']
                invTransactionDetailsData.NetAmount = invDetails['NetAmount']
                if invTransactionMasterData.VoucherType == 'PI' or invTransactionMasterData.VoucherType == 'PE' or invTransactionMasterData.VoucherType == 'SR':
                    invTransactionDetailsData.QtyIn = invDetails['Quantity']
                    invTransactionDetailsData.QtyOut = 0
                elif invTransactionMasterData.VoucherType == "SI" or invTransactionMasterData.VoucherType == 'SE' or invTransactionMasterData.VoucherType == 'PR':    
                    invTransactionDetailsData.QtyIn = 0
                    invTransactionDetailsData.QtyOut = invDetails['Quantity']
                elif invTransactionMasterData.VoucherType == 'SO' or invTransactionMasterData.VoucherType == 'PO' :
                    invTransactionDetailsData.QtyIn = 0
                    invTransactionDetailsData.QtyOut = 0                        
                invTransactionDetailsData.Remarks = invDetails['Remarks'] if 'Remarks' in invDetails else ''
                invTransactionDetailsData.save() 

            if(invTransactionMasterData.IsPosted == 1):
                #AccTransaction Master data 
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
                    accTransactionMasterData.InvTransactionMasterID =  models.InvTransactionMaster.objects.get(InvTransactionMasterID =latestInvTransactionID)
                    accTransactionMasterData.Particulars =  accMaster['AccountName']                   
                    accTransactionMasterData.TransactionDate = accMaster['TransactionDate']
                    accTransactionMasterData.SystemDate = currentDate
                    accTransactionMasterData.BankDate = accMaster['TransactionDate']
                    accTransactionMasterData.VoucherPrefix = accMaster['VoucherPrefix']
                    accTransactionMasterData.VoucherNumber = accMaster['VoucherNumber']
                    accTransactionMasterData.VoucherType  = accMaster['VoucherType']
                    accTransactionMasterData.VoucherForm   =  invMaster['VoucherForm']
                    accTransactionMasterData.ReferenceNumber = accMaster['ReferenceNo']
                    accTransactionMasterData.ReferenceDate = accMaster['ReferenceDate']
                    accTransactionMasterData.DueDate  = accMaster['DueDate']
                    accTransactionMasterData.PaymentMethord  = accMaster['PaymentMethord']
                    accTransactionMasterData.ActionStatus = "A"
                    if invTransactionMasterData.OldInvTransactionID > 0:
                        accTransactionMasterData.CreatedDate =  invMaster['CreatedDate']
                        accTransactionMasterData.ModifiedDate =  currentDate
                        message =  "Update successfully....!" 
                    elif invTransactionMasterData.OldInvTransactionID==0:
                        accTransactionMasterData.CreatedDate =  currentDate
                        accTransactionMasterData.ModifiedDate =  currentDate
                        message =  "Saved successfully....!"                    
                    if accTransactionMasterData.VoucherType == 'PI' or accTransactionMasterData.VoucherType == 'PE' or accTransactionMasterData.VoucherType == 'SR'or accTransactionMasterData.VoucherType == 'PO':
                        accTransactionMasterData.TotalDebit  = 0
                        accTransactionMasterData.TotalCredit  = TotalAmount
                    elif accTransactionMasterData.VoucherType == "SI" or accTransactionMasterData.VoucherType == 'SE' or accTransactionMasterData.VoucherType == 'PR' or accTransactionMasterData.VoucherType == 'SO' :
                        accTransactionMasterData.TotalDebit  = TotalAmount
                        accTransactionMasterData.TotalCredit  = 0
                        
                    accTransactionMasterData.TotDiscount  = TotalDiscount
                    accTransactionMasterData.CommonNarration  = Remarks
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
                    accTransactionDetailsData.Narration = accDetails['Narration']if 'Narration' in accDetails else ''
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
                    accTransactionDetailsData.Narration = accDetails['Narration']if 'Narration' in accDetails else ''
                    accTransactionDetailsData.save() 
            if  invTransactionMasterData.OldInvTransactionID > 0:
                invTransactionMasterEditData = models.InvTransactionMaster.objects.get(InvTransactionMasterID = invTransactionMasterData.OldInvTransactionID)
                accTransactionMasterEditData = models.AccTransactionMaster.objects.get(InvTransactionMasterID = invTransactionMasterData.OldInvTransactionID)
                invTransactionMasterEditData.IsActive = False
                invTransactionMasterEditData.ActionStatus = "E"
                accTransactionMasterEditData.IsActive = False
                accTransactionMasterEditData.ActionStatus = "E"
                invTransactionMasterEditData.save() 
                            
            responseOBJ = {"message":message, "type":"success"}
            # responseOBJ = {"message":message,  "type":"success"}  
        return HttpResponse(json.dumps(responseOBJ,default=str))   
        # return HttpResponse("Done")   
    except ValueError:
        return HttpResponse({"Not Saved":" Error in insertion....!", "type":"error"})

@api_view(['GET'])
def getTransactionMasterDataById(request,invTransactionMasterID):
    try:
        invTransactionMasterData = list(models.InvTransactionMaster.objects.filter(InvTransactionMasterID = invTransactionMasterID).values()) 
        return HttpResponse(json.dumps(invTransactionMasterData, default=str))       
    except(ValueError):        
        return HttpResponse("Error")

@api_view(['GET'])
def getTransactionDetailsDataById(request,invTransactionMasterID):
    try:
        invTransactionDetailsData = list(models.InvTransactionDetails.objects.filter(InvTransactionMasterID = invTransactionMasterID).values()) 
        return HttpResponse(json.dumps(invTransactionDetailsData, default=str))       
    except(ValueError):        
        return HttpResponse("Error")
@api_view(['GET'])
def fetchInvTransactionsForGrid(request,voucherType):
    try:
        # fetchAllTransData = models.InvTransactionMaster.objects.filter(ActionStatus = 'A', VoucherType = 'SE', IsPosted = True, IsActive = True).values()
        conn = psycopg2.connect(host="localhost",port="5432",database="polosysbookdb1001", user="postgres", password="root")
        cur = conn.cursor() # books_party."PartyID" books_party."PartyCode" books_party."Email" books_party."Phone" books_party."Mobile" books_party."OpeningBalance"
        cur.execute(""" SELECT books_invtransactionmaster."InvTransactionMasterID", books_invtransactionmaster."VoucherNumber", books_invtransactionmaster."TransactionDate",books_invtransactionmaster."ReferenceNo", books_invtransactionmaster."VoucherPrefix", books_invtransactionmaster."IsInvoiced", books_invtransactionmaster."DueDate", books_invtransactionmaster."DueDate", books_invtransactionmaster."GrandTotal", books_party."DisplayName"  FROM public.books_invtransactionmaster JOIN public.books_party ON books_invtransactionmaster."AccountID_id" = books_party."AccountID_id" WHERE books_invtransactionmaster."VoucherType" = """ + "'" +voucherType + """' AND "ActionStatus"='A' AND "IsActive"=true """ )
        row_headers=[x[0] for x in cur.description]
        row = cur.fetchall()
        result_data=[]
        for result in row:
            result_data.append(dict(zip(row_headers,result)))
        return HttpResponse(json.dumps(result_data, default=str))
        # return HttpResponse(json.dumps(fetchAllTransData,default=str))
    except(ValueError):        
        return HttpResponse("Error")
@api_view(['GET'])
def getTransactionDataById(request,invTransactionMasterID):
    try:
        invTransactionMasterData = list(models.InvTransactionMaster.objects.filter(InvTransactionMasterID = invTransactionMasterID).values()) 
        invTransactionDetailsData = list(models.InvTransactionDetails.objects.filter(InvTransactionMasterID = invTransactionMasterID).values()) 
        data={}
        data["master"]=invTransactionMasterData
        data["details"]=invTransactionDetailsData
        return HttpResponse(json.dumps(data, default=str))       
    except(ValueError):        
        return HttpResponse("Error")
@api_view(['GET'])
def delete(request,id):
    try:
        transModel = models.InvTransactionMaster.objects.get(InvTransactionMasterID = id)
        print(transModel)
        accTrnsModel = models.AccTransactionMaster.objects.get(InvTransactionMasterID = id)
        transModel.IsActive = False
        accTrnsModel.IsActive = False
        transModel.ActionStatus = 'D'
        accTrnsModel.ActionStatus = 'D'
        transModel.save()
        accTrnsModel.save()       
        responseOBJ = {"message": "delete successfully....!", "type":"success"}
    except ValueError:
        return Response({"message":" error Occur....!", "type":"error"})
    return HttpResponse(json.dumps(responseOBJ)) 

def checkDuplicateRefNo(request,referenceNo,partyAccID):
    try:
        isDuplicateRefNo = models.InvTransactionMaster.objects.filter(AccountID=partyAccID,ReferenceNo = referenceNo)
        if isDuplicateRefNo:
            responseOBJ = {"isDuplicate":True,"message":"Reference number is already exist in same party", "type":"success"}
        elif not isDuplicateRefNo:
            responseOBJ = {"isDuplicate":False,"message":"No Duplicate Reference No", "type":"success"}
        
    except(ValueError):
        responseOBJ = {"isDuplicate":False,"message":"Error Occur....!", "type":"error"}
    return HttpResponse(json.dumps(responseOBJ))    
