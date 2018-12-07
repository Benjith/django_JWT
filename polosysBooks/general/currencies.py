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
def saveCurrencyDetails(request):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        currencyData = models.Currencies()
        lastid = models.Currencies.objects.last()
        if lastid:
            currencyData.CurrencyID = lastid.CurrencyID+1
        elif not lastid:
            currencyData.CurrencyID = 1
        currencyData.BranchID = models.Branch.objects.get(BranchID = 1)
        currencyData.CountryID = models.Country.objects.get(CountryID = data['CountryID'])
        currencyData.CurrencyCode =  data['CurrencyCode']
        currencyData.CurrencyName = data['CurrencyName']
        currencyData.CurrencySymbol = data['CurrencySymbol']
        currencyData.SubUnit = data['SubUnit']
        currencyData.SubUnitSymbol  = data['SubUnitSymbol']
        currencyData.Remarks = data['Remarks']
        currencyData.save()
        responsOBJ = {"type":"success","message":"saved successfully"}
    except(ValueError):
        responsOBJ = {"type":"error","message":"erro occur...!"}
    return HttpResponse(json.dumps(responsOBJ))

# Delete Currencies
@api_view(['POST','GET'])
def deleteCurrency(request,currency_id):
    try:
        models.Currencies.objects.get(CurrencyID=currency_id).delete()
        responseOBJ = {"type":"success","message":"Delete Successfully...!"}
    except(ValueError):
        responseOBJ = {"type":"error","message":"Error occur in deletion...!"}
    return HttpResponse(json.dumps(responseOBJ))
    # CurrencyID  BranchID CountryID CurrencyCode CurrencyName CurrencySymbol SubUnit SubUnitSymbol Remarks