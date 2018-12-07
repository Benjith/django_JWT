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

# insert
@api_view(['POST'])
def saveWarehouse(request):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        wareHouse = models.Warehouse()
        if 'WarehouseID' in data :
            print("update")
        else :
            latest = models.Warehouse.objects.last()
            if latest:
                wareHouse.WarehouseID = latest.WarehouseID+1
            elif not latest:
                wareHouse.WarehouseID = 1
        wareHouse.BranchID=models.Branch.objects.get(pk=data['BranchID']) if 'BranchID' in data else 1
        wareHouse.WarehouseName=data['WarehouseName'] if 'WarehouseName' in data else "" 
        wareHouse.WarehouseType = data['WarehouseType'] if 'WarehouseType' in data else ""
        wareHouse.Warehouselocation = data['Warehouselocation'] if 'Warehouselocation' in data else ""
        wareHouse.Remarks=data['Remarks'] if 'Reamrks' in data else ""
        wareHouse.IsActive=data['isActive'] if 'isActive' in data else True
        wareHouse.save()
        responseOBJ = {"message":" saved successfully....!", "success":True}
    except ValueError:
        return Response({"message":" Error in insertion....!", "success":False})
    return Response(responseOBJ)
   
#get    
@api_view(['GET'])
def getWarehouse(request):
    try:
        responseOBJ = list(models.Warehouse.objects.values())
        return HttpResponse(json.dumps(responseOBJ))
    except ValueError:
        return Response(json.dumps("Sorry, an unknown error happened"))   
#delete            
@api_view(['GET'])
def deleteWarehouse(request,warehouseid):
    try:
        models.Warehouse.objects.get(id=warehouseid).delete()
        responseOBJ = {"message":"Delete successfully....!", "type":"success"}
        return Response(responseOBJ)       
    except ValueError:
        return HttpResponse({"message": "Error in delete","type" :"error" })
#update            
@api_view(['POST'])
def updateWarehouse(request):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        warehouse = models.Warehouse()
        warehouse.WarehouseID = models.Warehouse.objects.get(WarehouseID=data['UpdateID'])
        warehouse.BranchID=models.Branch.objects.get(BranchID=data['branchID'])
        warehouse.WarehouseName=data['warehouseName']
        warehouse.WarehouseType=data['warehouseType']        
        warehouse.Warehouselocation=data['warehouselocation']        
        warehouse.Remarks = data['remarks']
        warehouse.save()
        responseOBJ = {"message":"updated successfully....!", "type":"success"} 
        return Response(responseOBJ)        
    except ValueError:
        return HttpResponse({"message": "Error in updation","type" :"error" })