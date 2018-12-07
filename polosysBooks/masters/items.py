from django.http import HttpResponse
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from io import BytesIO
from rest_framework.parsers import JSONParser
import json
import psycopg2
from django.http import JsonResponse
import sys
sys.path.append('..')
import polosysBooks
from polosysBooks import models


#insert or update Item   
@api_view(['POST'])   
def insertOrUpdateItem(request):
  try:
      data = BytesIO(request.body)
      data = JSONParser().parse(data)
      ItemModel= models.Items()
      #check if insertion or updation 
      if 'ItemID' not in data:
        latest = models.Items.objects.last()
        if latest:
          ItemModel.ItemID = latest.ItemID+1
        elif not latest:
          ItemModel.ItemID = 1
      else: 
        ItemModel.ItemID=data['ItemID']
      ItemModel.BranchID=models.Branch.objects.get(pk=data['BranchID'])
      ItemModel.ItemCode=data['ItemCode'] if'ItemCode' in data else ""
      ItemModel.ItemName=data['ItemName'] if'ItemCode' in data else ""
      ItemModel.ItemType=data['ItemType'] if'ItemCode' in data else ""
      ItemModel.ItemSubCategoryID=models.ItemSubCategory.objects.get(pk=data['ItemSubCategoryID']) 
      ItemModel.UnitID=models.UnitOfMeasures.objects.get(pk=data['UnitID'])
      ItemModel.TaxCategoryID=models.TaxCategory.objects.get(pk=data['TaxCategoryID'])
      ItemModel.PurchaseRate=data['PurchaseRate'] if 'PurchaseRate' in data else ""
      ItemModel.SalesRate=data['SalesRate'] if 'PurchaseRate' in data else ""
      ItemModel.HSNCode=data['HSNCode'] if 'HSNCode' in data else ""
      ItemModel.EAN_SKU=data['EAN_SKU'] if 'EAN_SKU' in data else ""
      ItemModel.OpeningStock=data['OpeningStock'] if 'OpeningStock' in data else ""
      ItemModel.OpeningDate=data['OpeningDate'] if 'OpeningDate' in data else ""
      ItemModel.AccountID=models.ChartofAccounts.objects.get(pk=data['PartyID']) 
      ItemModel.MaintainInventory=True
      ItemModel.ItemURL=data["ItemURL"] if 'ItemURL' in data else "No Image"
      ItemModel.LastPurchaseRate=data['LastPurchaseRate'] if 'lastPurchaseRate' in data else 0
      ItemModel.LastPurchaseCost=data['LastPurchaseCost'] if 'LastPurchaseCost' in data else 0
      ItemModel.AvgRate=data['AvgRate'] if 'AvgRate' in data else 0
      ItemModel.FIFOValue=data['FIFOValue'] if 'FIFOValue' in data else 0
      ItemModel.Remarks=data['Remarks'] if 'Remarks' in data else 0
      ItemModel.save()
    
      responseOBJ={ "success":True,"message":"Item Added" }
  except ValueError as err:
    responseOBJ={ "success":False,"message":err }
  return HttpResponse(json.dumps(responseOBJ, default=str))
@api_view(["POST"])
def imageUpload(request):
    folder = request.path.replace("/", "_")
    uploaded_filename = request.FILES['file'].name

    # create the folder if it doesn't exist.
    try:
        os.mkdir(os.path.join(BASE_PATH, folder))
    except:
        pass

    # save the uploaded file inside that folder.
    full_filename = os.path.join(BASE_PATH, folder, uploaded_filename)
    fout = open(full_filename, 'wb+')
    # Iterate through the chunks.
    for chunk in fout.chunks():
        fout.write(chunk)
    fout.close()
    return HttpResponse("DONE")

@api_view(["GET"])
def listAllItems(request):
    # responseOBJ = list(models.Items.objects.select_related('UnitID'))
    # for i in responseOBJ:
    #  print(i.ItemName)
    #  print( i.UnitID.UnitName)
    # return HttpResponse(json.dumps(responseOBJ.UnitID,default=str))

    conn = psycopg2.connect(host="localhost",database="polosysbookdb1001", user="postgres", password="root")
    cur = conn.cursor() 
    cur.execute(""" SELECT * FROM public.books_items JOIN public.books_UnitOfMeasures ON books_Items."UnitID_id" = books_UnitOfMeasures."UnitID" JOIN public.books_ItemSubCategory ON books_ItemSubCategory."ItemSubCategoryID" =books_Items."ItemSubCategoryID_id"  """)
    row_headers=[x[0] for x in cur.description]
    row = cur.fetchall()
    result_data=[]
    for result in row:
        result_data.append(dict(zip(row_headers,result)))
    return HttpResponse(json.dumps(result_data, default=str))
def deleteById(request,itemID):
  try:
        models.Items.objects.get(ItemID=itemID).delete()
        responseOBJ = {"message": "Delete successfully....!", "success":True}
  except(ValueError):
        responseOBJ = {"success":False,"message":"Error occur in deletion...!"}
  return HttpResponse(json.dumps(responseOBJ))
@api_view(["GET"])
def deleteImageByName(request ,imageName):
  print(imageName)
  try:
    models.ImgUpload.objects.get(img="Pic/"+imageName).delete()
    responseOBJ = {"message": "Delete successfully....!", "success":True}
  except (ValueError):
    responseOBJ = {"success":False,"message":"Error occur in deletion...!"}
  return HttpResponse(json.dumps(responseOBJ))
  
@api_view(['GET'])
def fetchAllItem(request,itemType):
  try:
    fetchAllItem = list(models.Items.objects.filter(ItemType = itemType).values())
    responseOBJ = fetchAllItem
  except(ValueError):
    responseOBJ = {"message":"Error occur .....!","type":"error"}
  return HttpResponse(json.dumps(fetchAllItem, default=str))

@api_view(['GET'])
def fetchItemByID(request,itemID):
  try:
    fetchAllItem = list(models.Items.objects.filter(ItemID = itemID).values())
    responseOBJ = fetchAllItem
  except(ValueError):
    responseOBJ = {"message":"Error occur .....!","type":"error"}
  return HttpResponse(json.dumps(fetchAllItem, default=str))

@api_view(['GET'])
def getItemByItemCode(request,ItemCode):
  try:
    fetchAllItem = list(models.Items.objects.filter(ItemCode = ItemCode).values())
    responseOBJ = fetchAllItem
  except(ValueError):
    responseOBJ = {"message":"Error occur .....!","type":"error"}
  return HttpResponse(json.dumps(fetchAllItem, default=str))

@api_view(['GET'])
def getItemByEAN_SKU(request,EAN_SKU):
  try:
    fetchAllItem = list(models.Items.objects.filter(EAN_SKU = EAN_SKU).values())
    responseOBJ = fetchAllItem
  except(ValueError):
    responseOBJ = {"message":"Error occur .....!","type":"error"}
  return HttpResponse(json.dumps(fetchAllItem, default=str))


