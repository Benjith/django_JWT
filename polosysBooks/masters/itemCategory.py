from django.http import HttpResponse
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from io import BytesIO
from rest_framework.parsers import JSONParser
import json
from django.http import JsonResponse
import sys
sys.path.append('..')
import polosysBooks
from polosysBooks import models

@api_view(['POST']) 
#insert new item categopry
def addNewItemCategory(request):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        itemSubModel= models.ItemSubCategory()
        latest = models.ItemSubCategory.objects.last()
        if latest:
          itemSubModel.ItemSubCategoryID = latest.ItemSubCategoryID+1
        elif not latest:
          itemSubModel.ItemSubCategoryID = 1
        itemSubModel.BranchID=models.Branch.objects.get(pk=data['BranchID'])
        itemSubModel.ItemCategoryID=models.ItemCategory.objects.get(pk=data['ItemCategoryID'])
        itemSubModel.ItemSubCategoryName=data['ItemSubCategoryName']
        itemSubModel.Remarks=data['Remarks']
        itemSubModel.save()
        responseOBJ={ "success":True,"message":"Saved Succesfully" }

    except ValueError as err:
      responseOBJ={ "success":False,"message":err }
    return HttpResponse(json.dumps(responseOBJ, default=str))





@api_view(["GET"])
def listAllMainCategory(request):
  responseOBJ = list(models.ItemCategory.objects.values())
  return HttpResponse(json.dumps(responseOBJ))
def listAllSubCategory(request):
  responseOBJ = list(models.ItemSubCategory.objects.values())
  return HttpResponse(json.dumps(responseOBJ))
