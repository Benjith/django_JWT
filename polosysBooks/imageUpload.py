from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from . import models

@api_view(["POST"])
def ItemImgUpload(request):
    try:
        if request.method == 'POST' :
            myfile = request.data['file']
            fileModel= models.ImgUpload(img=myfile,remark="Nothing")
            fileModel.save()
            # return HttpResponse("{Success:True}")
            return HttpResponse(status=204)
        else :
            print("No file found ")
    except ValueError as msg:
        return HttpResponse("{error:"+msg+"}")