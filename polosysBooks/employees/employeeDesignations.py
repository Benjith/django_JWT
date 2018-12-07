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
def saveEmployeeDesignation(request):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        print(data)
        empDesignation = models.EmployeeDesignation()
        lastid = models.EmployeeDesignation.objects.last()
        # print(lastid.EmployeeDesignationID)
        if lastid is None:
            empDesignation.EmployeeDesignationID = 1
        elif lastid:            
            empDesignation.EmployeeDesignationID = lastid.EmployeeDesignationID + 1         
        empDesignation.BranchID=models.Branch.objects.get(BranchID=data['branchID'])
        empDesignation.EmployeeDesignationName=data['employeedesignationName']
        empDesignation.ShortName=data['shortName']
        empDesignation.Remarks = data['remarks']
        empDesignation.save()
        responseOBJ = {"message":" saved successfully....!", "type":"success"}
        
    except ValueError:
        return Response({"message":" Error in insertion....!", "type":"error"})
    return Response(responseOBJ)
#get    
@api_view(['GET'])
def getEmployeeDesignation(request):
    try:
        responseOBJ = list(models.EmployeeDesignation.objects.values())
        return HttpResponse(json.dumps(responseOBJ))
    except ValueError:
        return Response(json.dumps("Sorry, an unknown error happened")) 
#delete            
@api_view(['GET'])
def deleteEmployeeDesignation(request,deleteId):
    try:
        models.EmployeeDesignation.objects.get(EmployeeDesignationID=deleteId).delete()
        responseOBJ = {"message":"Delete successfully....!", "type":"success"}
        return Response(responseOBJ)       
    except ValueError:
        return HttpResponse({"message": "Error in delete","type" :"error" })
#update            
@api_view(['POST'])
def updateEmployeeDesignation(request,updateId):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        print(data)
        empDesignation = models.EmployeeDesignation()
        empDesignation.EmployeeDesignationID = models.EmployeeDesignation.objects.get(EmployeeDesignationID=updateId)
        empDesignation.BranchID=models.Branch.objects.get(BranchID=data['branchID'])
        empDesignation.EmployeeDesignationName=data['employeedesignationName']
        empDesignation.ShortName=data['shortName']
        empDesignation.Remarks = data['remarks']
        empDesignation.save()
        responseOBJ = {"message":"updated successfully....!", "type":"success"}   
        return Response(responseOBJ)       
    except ValueError:
        return HttpResponse({"message": "Error in updation","type" :"error" })
                   
    
