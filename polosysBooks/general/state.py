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

# Fetch All State
@api_view(['GET'])
def fetchAllState(request,CountryID):
    try:
        fetchAllState = list(models.State.objects.filter(CountryID = CountryID).values())
        return HttpResponse(json.dumps(fetchAllState, default=str))
    except(ValueError) as er:
        return HttpResponse("Error Occur...!")