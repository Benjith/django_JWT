from django.http import HttpResponse
import json
import sys
sys.path.append('..')
import polosysBooks
from polosysBooks import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from io import BytesIO
from rest_framework.parsers import JSONParser
from django.conf import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
from django.core.management import call_command
from django.utils import timezone
import datetime

@api_view(['POST','GET'])
def saveAccType(request):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        print(data)
        dataAndTime=timezone.now()
        accTypeLatestID = models.AccountType.objects.last()
        accTypeData = models.AccountType()
        if accTypeLatestID:
            accTypeData.AccountTypeID = accTypeLatestID.AccountTypeID+1            
        elif not accTypeLatestID:
            accTypeData.AccountTypeID = 1001
        print(accTypeData.AccountTypeID)

        #set account type code
        # get 
        getParentTypeCode = models.AccountType.objects.get(AccountTypeID=data['ParentTypeID'])
        parentTypeCode = getParentTypeCode.AccountTypeCode
        # Count total no.of parent type id
        accTypeCodeCount = models.AccountType.objects.filter(ParentTypeID=data['ParentTypeID']).count()
        print(accTypeCodeCount)

        # create account type code 
        createdAccTypeCode = parentTypeCode+'-'+str(accTypeCodeCount+1)
        # {"AccountTypeID":"1001","BranchID":"1" , "AccountTypeCode":"1220", "AccountTypeName":"Ledger", "ParentTypeID":"1", "Remarks":"1", "isProtected":"0"}
        # AccountTypeID BranchID AccountTypeCode AccountTypeName ParentTypeID Remarks isProtected
        accTypeData.BranchID = models.Branch.objects.get(pk = 1)
        accTypeData.AccountTypeCode = createdAccTypeCode
        accTypeData.AccountTypeName = data['AccountTypeName']
        accTypeData.ParentTypeID = data['ParentTypeID']
        accTypeData.Remarks = data['Remarks']
        accTypeData.isProtected = 0
        accTypeData.save()
        reponseOBJ = {"type":"Success","message":"Account type saved successfully"}
    except(ValueError) as er:
        reponseOBJ = {"type":"Error" , "message":"Error occur "}
    return HttpResponse(json.dumps(reponseOBJ))


@api_view(['GET'])
def fetchAllAccType(request):
    try:
        fetchAllAccTypeData = list(models.AccountType.objects.values())    
        return HttpResponse(json.dumps(fetchAllAccTypeData))
    except(ValueError):
        return HttpResponse("Error occur")

# DELETE ACCOUNT TYPE
@api_view(['GET'])
def deleteAccType(request,accType_id):
    try:
        is_protected = models.AccountType.objects.get(AccountTypeID=accType_id)
        if is_protected.isProtected == True:
            responseOBJ = {"message": str(is_protected.AccountTypeName)+"   is protected....!", "type":"warning"}
        elif is_protected.isProtected == False:
            models.AccountType.objects.get(AccountTypeID=accType_id,isProtected = False).delete()
            responseOBJ = {"message": "Delete successfully....!", "type":"success"}
    except(ValueError):
        responseOBJ = {"type":"error","message":"Error occur in deletion...!"}
    return HttpResponse(json.dumps(responseOBJ))