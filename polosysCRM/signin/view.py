import jwt,json
from rest_framework import views
from rest_framework.response import Response
import sys
sys.path.append('..')
from polosysCRM import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from io import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework_jwt.settings import api_settings
from django.conf import settings

@api_view(['POST'])
# @permission_classes([AllowAny, ])
def authenticate_user(request):
 
    try:
        email = request.data['email']
        password = request.data['password']
 
        user = models.Users.objects.get(email=email, password=password)
        if user:
            try:
                payload = {
                # 'id': user.id,
                'email': user.email,
            }
                jwt_token =  {'token': jwt.encode(payload, "SECRET_KEY")}
                return HttpResponse(json.dumps(jwt_token,default=str))
 
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return HttpResponse(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return HttpResponse(res) 