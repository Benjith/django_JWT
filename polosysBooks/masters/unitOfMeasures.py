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
def addUnitOfMeasures(request):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        UnitModel = models.UnitOfMeasures()
        if 'TaxCategoryID' in data :
            print("update")
        else :
            latest = models.UnitOfMeasures.objects.last()
            if latest:
                UnitModel.UnitID = latest.UnitID+1
            elif not latest:
                UnitModel.UnitID = 1
        UnitModel.BranchID=models.Branch.objects.get(pk=data['BranchID']) if 'BranchID' in data else 1
        UnitModel.UnitCode=data['UnitCode'] if 'UnitCode' in data else ""
        UnitModel.UnitName = data['UnitName'] if 'UnitName' in data else ""
        UnitModel.Remarks = data['remarks'] if 'remarks' in data else ""       
        UnitModel.save()
        responseOBJ = {"message":" saved successfully....!", "success":True}
        
    except ValueError:
        return Response({"message":" Error in insertion....!", "success":False})
    return Response(responseOBJ)
# get     
@api_view(['GET'])
def listAllUnit(request):
  responseOBJ= list(models.UnitOfMeasures.objects.values())
  return HttpResponse(json.dumps(responseOBJ,default=str))
