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
from dynamic_db_router import in_database

dbname = 'polosysbooksdb1002'
externa_db = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME' : dbname,
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }

@api_view(['POST','GET'])
def saveCurrencyDetails(request):
    with in_database(externa_db,write=True):
        userData = models.Branch()
        lastid = models.Branch.objects.last()
        if lastid:
            userData.BranchID = lastid.BranchID + 1
        elif not lastid:
            userData.BranchID = 1
        userData.BranchCode = 'B1'
        userData.BranchName = 'Branch 1'
        userData.Remarks = 'rem1'
        userData.save()
        fetchallUser = list(models.Branch.objects.values())
        print(externa_db['NAME'])
        print(fetchallUser)
    return HttpResponse("ok")