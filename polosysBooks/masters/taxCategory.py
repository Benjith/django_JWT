from django.http import HttpResponse
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from io import BytesIO
from rest_framework.parsers import JSONParser
import simplejson as json
import sys
sys.path.append('..')
import polosysBooks
from polosysBooks import models

# insert
@api_view(['POST'])
def saveTaxCategory(request):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        taxCategory = models.TaxCategory()
        if 'TaxCategoryID' in data :
            print("update")
        else :
            latest = models.TaxCategory.objects.last()
            if latest:
                taxCategory.TaxCategoryID = latest.TaxCategoryID+1
            elif not latest:
                taxCategory.TaxCategoryID = 1
        taxCategory.BranchID=models.Branch.objects.get(pk=data['BranchID']) if 'BranchID' in data else 1
        taxCategory.TaxCategoryName=data['TaxCategoryName'] if 'TaxCategoryName' in data else 0 
        taxCategory.SalesVatPerc = data['SalesVatPerc'] if 'SalesVatPerc' in data else 0
        taxCategory.PurchaseVatPerc = data['PurchaseVatPerc'] if 'PurchaseVatPerc' in data else 0
        taxCategory.SalesCessPerc=data['SalesCessPerc'] if 'SalesCessPerc' in data else 0
        taxCategory.PurchaseCessPerc=data['PurchaseCessPerc'] if 'PurchaseCessPerc' in data else 0
        taxCategory.SalesSGSTPerc = data['SalesSGSTPerc'] if 'SalesSGSTPerc' in data else 0
        taxCategory.PurchaseSGSTPerc = data['PurchaseSGSTPerc'] if 'PurchaseSGSTPerc' in data else 0
        taxCategory.SalesCGSTPerc=data['SalesCGSTPerc'] if 'SalesCGSTPerc' in data else 0
        taxCategory.PurchaseCGSTPerc=data['PurchaseCGSTPerc'] if 'PurchaseCGSTPerc' in data else 0
        taxCategory.SalesIGSTPerc = data['SalesIGSTPerc'] if 'SalesIGSTPerc' in data else 0
        taxCategory.PurchaseIGSTPerc = data['PurchaseIGSTPerc'] if 'PurchaseIGSTPerc' in data else 0
        taxCategory.Remarks = data['remarks'] if 'remarks' in data else ""       
        taxCategory.save()
        responseOBJ = {"message":" saved successfully....!", "success":True}
        
    except ValueError:
        return Response({"message":" Error in insertion....!", "success":False})
    return Response(responseOBJ)
# get     
@api_view(['GET'])
def getTaxCategory(request):
    try:
        responseOBJ = list(models.TaxCategory.objects.values())
        return HttpResponse(json.dumps(responseOBJ))
    except ValueError:
        return Response(json.dumps("Sorry, an unknown error happened")) 
#delete        
@api_view(['GET'])
def deleteTaxCategory(request,taxCategoryid):
    try:
        models.TaxCategory.objects.get(id=taxCategoryid).delete()
        responseOBJ = {"message":"Delete successfully....!", "success":True}
        return Response(responseOBJ)       
    except ValueError:
            return HttpResponse({"message": "Error in delete","success" :False})
# update
@api_view(['POST'])
def updateTaxCategory(request):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        taxCategory = models.TaxCategory()
        taxCategory.TaxCategoryID = models.TaxCategory.objects.get(TaxCategoryID=data['UpdateID'])
        taxCategory.BranchID==models.Branch.objects.get(BranchID=data['branchID'])
        taxCategory.TaxCategoryName=data['taxCategoryName']
        taxCategory.SalesVatPerc = data['salesVatPerc']
        taxCategory.PurchaseVatPerc = data['purchaseVatPerc']
        taxCategory.SalesCessPerc=data['salesCessPerc']
        taxCategory.PurchaseCessPerc=data['purchaseCessPerc']
        taxCategory.SalesSGSTPerc = data['salesSGSTPerc']
        taxCategory.PurchaseSGSTPerc = data['purchaseSGSTPerc']
        taxCategory.SalesCGSTPerc=data['salesCGSTPerc']
        taxCategory.PurchaseCGSTPerc=data['purchaseCGSTPerc']
        taxCategory.SalesIGSTPerc = data['salesIGSTPerc']
        taxCategory.PurchaseIGSTPerc = data['purchaseIGSTPerc']
        taxCategory.Remarks = data['remarks']
        taxCategory.save()
        responseOBJ = {"message":"updated successfully....!", "success":True} 
        return Response(responseOBJ)         
    except ValueError:
        return HttpResponse({"message": "Error in updation","success" :False })
        
@api_view(['GET'])
def getTaxCategoryById(request,TaxCatID):
    try:
        responseOBJ = list(models.TaxCategory.objects.filter(TaxCategoryID = TaxCatID).values())
        return HttpResponse(json.dumps(responseOBJ))
    except ValueError:
        return Response(json.dumps("Sorry, an unknown error happened")) 