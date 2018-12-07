from django.http import HttpResponse
import json
import sys
sys.path.append('..')
from polosysCRM import models
import polosysCRM

from rest_framework.decorators import api_view
from rest_framework.response import Response
from io import BytesIO
from rest_framework.parsers import JSONParser
from django.core.mail import EmailMessage
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
from django.core.management import call_command
from django.utils import timezone
import datetime
from polosysBooks.models import Users
import csv
from dynamic_db_router import in_database

# externa_db = {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME' : 'polosysbookdb1000',
#     'USER': 'postgres',
#     'PASSWORD': 'root',
#     'HOST': 'localhost',
#     'PORT': '5432',
# }

@api_view(['POST'])
def saveCustomer(request):
    try:
        data = BytesIO(request.body)
        data = JSONParser().parse(data)
        # get current data and time with time zone
        dataAndTime=timezone.now()
        customersLast_id = models.Customers.objects.last()    
        customerData = models.Customers()
        
        #checking customer table is empty or not, if it is not empty get last id and set customer id is equal to lastid++ or else customer  id is 1001 
        if customersLast_id:
            customerData.CustomerID = customersLast_id.CustomerID+1
        elif not customersLast_id:
            customerData.CustomerID = 1001
        
        customerData.CustomerFName = data['fullName']
        customerData.Email = data['email']
        customerData.CreatedDate = str(dataAndTime)
        customerData.ExpiryDate = str(dataAndTime)
        customerData.FirstLoggedDate = str(dataAndTime)
        customerData.RenewalDate = dataAndTime
        customerData.BranchID = models.Branch.objects.get(pk = 1)
        customerData.CountryID = models.Country.objects.get(pk = 1)
        customerData.save()
        # get latest insert id
        customerLatestInsertID = getCustomerLatestId()

        # call table creation function
        dbName = 'polosysbooksdb'+str(customerLatestInsertID)       
        isDbCreated = customerDbCreator(dbName)
        if isDbCreated == True:
            print('dbcreate successfully')
            settings.DATABASES['polosysBooksDB']['NAME'] = dbName            
            call_command("migrate",database='polosysBooksDB', interactive = False)
            # add to database info table
            try:
                lastInsertedID = models.Customers.objects.last()
                usersLast_id = models.Users.objects.last()

                databaseInfo= models.DatabaseInfo()
                databaseInfo.CustomerID = models.Customers.objects.get(pk=lastInsertedID.CustomerID)
                databaseInfo.ProductID = models.Products.objects.get(ProductID=1)
                databaseInfo.DatabaseName = dbName
                databaseInfo.Host = "localhost"
                databaseInfo.Port = "5432"
                databaseInfo.Username = "postgres"
                databaseInfo.Password = "root"
                databaseInfo.save()
               
            # add to user table  
           
               
                userData = models.Users()
                if usersLast_id:
                    userData.UserID = usersLast_id.UserID+1
                elif not usersLast_id:
                    userData.UserID = 1001
                print(userData.UserID)
                userData.BranchID = models.Branch.objects.get(BranchID = 1)
                userData.username = data['fullName']
                userData.email = data['email']
                userData.password = data['password']
                userData.CustomerID = models.Customers.objects.get(pk=lastInsertedID.CustomerID)
                userData.ProductID =  models.Products.objects.get(ProductID=1)
                userData.CreatedDate = dataAndTime
                userData.ExpiryDate = dataAndTime
                userData.FirstLoggedDate = dataAndTime
                userData.IsActive = True
                userData.IsAdmin = True
                userData.last_login =dataAndTime    
                userData.date_joined =dataAndTime    
                userData.is_superuser =False    
                userData.save()
                            
                #sent mail
                sendMail(data)
            except(ValueError):
                return False
        else:
            print('error occur in db creation')

        responseOBJ = {"message": " Registration successfully completed....!", "type":"success"}
    except(ValueError) as msg:
        responseOBJ= {"message":msg, "type":"error"} 
    return HttpResponse(json.dumps(responseOBJ , default=str))


# # Get customer latest insert id 
def getCustomerLatestId():
    lastInsertedID = models.Customers.objects.last()
    lastid = (lastInsertedID.CustomerID)
    return lastid

#  New DB creator function
def customerDbCreator(dbname):
    try:
        con = psycopg2.connect(dbname='postgres',
        user='postgres', host='localhost',
        password='root')
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

        cur = con.cursor()
        cur.execute("CREATE DATABASE %s  ;" % dbname)
        return True

    except(TypeError):
        return False

#check email is already exist or not in customer table
@api_view(['GET'])
def emailAlreadyExist(request,emailid):
    print(emailid)
    emailCheck =  models.Customers.objects.filter(Email=emailid)
    if emailCheck:
        isEmailExist = {'isExist':True}
    else:
        isEmailExist = {'isExist':False}
    print(isEmailExist)
    return HttpResponse(json.dumps(isEmailExist))
def sendMail(data):
#Sent Email for verification 
                subject = "Activate your polosysbooks "+data['fullName']
                from_email = "mpbenjith@gmail.com"
                to = data['email']
                text_content = 'This is an important message.'
                html_content = "<!DOCTYPE html><html lang='en'><head> <meta charset='UTF-8'> <meta content='width=device-width, initial-scale=1' name='viewport'> <meta name='x-apple-disable-message-reformatting'> <meta http-equiv='X-UA-Compatible' content='IE=edge'> <meta content='telephone=no' name='format-detection'> <title></title> <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css integrity=' sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm ' crossorigin='anonymous '> <script src='https://code.jquery.com/jquery-3.2.1.slim.min.js ' integrity='sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN ' crossorigin='anonymous '></script><script src='https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js ' integrity='sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q ' crossorigin='anonymous '></script><script src='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js ' integrity='sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl ' crossorigin='anonymous '></script> <link href='https://fonts.googleapis.com/css?family=Open+Sans:400,400i,700,700i ' rel='stylesheet '></head><style>#outlook a{padding: 0;}.ExternalClass{width: 100%;}.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div{line-height: 100%;}.es-button{mso-style-priority: 100 !important;text-decoration: none !important;}a[x-apple-data-detectors]{color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important;}.es-desk-hidden{display: none; float: left; overflow: hidden; width: 0; max-height: 0; line-height: 0; mso-hide: all;}/*END OF IMPORTANT*/html,body{width: 100%; font-family: 'open sans ', 'helvetica neue ', helvetica, arial, sans-serif; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;}table{mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: collapse; border-spacing: 0px;}table td,html,body,.es-wrapper{padding: 0; Margin: 0;}.es-content,.es-header,.es-footer{table-layout: fixed !important; width: 100%;}img{display: block; border: 0; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;}table tr{border-collapse: collapse;}p,hr{Margin: 0;}h1,h2,h3,h4,h5{Margin: 0; line-height: 120%; mso-line-height-rule: exactly; font-family: 'open sans ', 'helvetica neue ', helvetica, arial, sans-serif;}p,ul li,ol li,a{-webkit-text-size-adjust: none; -ms-text-size-adjust: none; mso-line-height-rule: exactly;}.es-left{float: left;}.es-right{float: right;}.es-p5{padding: 5px;}.es-p5t{padding-top: 5px;}.es-p5b{padding-bottom: 5px;}.es-p5l{padding-left: 5px;}.es-p5r{padding-right: 5px;}.es-p10{padding: 10px;}.es-p10t{padding-top: 10px;}.es-p10b{padding-bottom: 10px;}.es-p10l{padding-left: 10px;}.es-p10r{padding-right: 10px;}.es-p15{padding: 15px;}.es-p15t{padding-top: 15px;}.es-p15b{padding-bottom: 15px;}.es-p15l{padding-left: 15px;}.es-p15r{padding-right: 15px;}.es-p20{padding: 20px;}.es-p20t{padding-top: 20px;}.es-p20b{padding-bottom: 20px;}.es-p20l{padding-left: 20px;}.es-p20r{padding-right: 20px;}.es-p25{padding: 25px;}.es-p25t{padding-top: 25px;}.es-p25b{padding-bottom: 25px;}.es-p25l{padding-left: 25px;}.es-p25r{padding-right: 25px;}.es-p30{padding: 30px;}.es-p30t{padding-top: 30px;}.es-p30b{padding-bottom: 30px;}.es-p30l{padding-left: 30px;}.es-p30r{padding-right: 30px;}.es-p35{padding: 35px;}.es-p35t{padding-top: 35px;}.es-p35b{padding-bottom: 35px;}.es-p35l{padding-left: 35px;}.es-p35r{padding-right: 35px;}.es-p40{padding: 40px;}.es-p40t{padding-top: 40px;}.es-p40b{padding-bottom: 40px;}.es-p40l{padding-left: 40px;}.es-p40r{padding-right: 40px;}.es-menu td{border: 0;}.es-menu td a img{display: inline !important;}/* END CONFIG STYLES */a{font-family: 'open sans ', 'helvetica neue ', helvetica, arial, sans-serif; font-size: 15px; text-decoration: none;}h1{font-size: 36px; font-style: normal; font-weight: bold; color: #333333;}h1 a{font-size: 36px;}h2{font-size: 30px; font-style: normal; font-weight: bold; color: #333333;}h2 a{font-size: 30px;}h3{font-size: 20px; font-style: normal; font-weight: bold; color: #333333;}h3 a{font-size: 20px;}p,ul li,ol li{font-size: 15px; font-family: 'open sans ', 'helvetica neue ', helvetica, arial, sans-serif; line-height: 150%;}ul li,ol li{Margin-bottom: 15px;}.es-menu td a{text-decoration: none; display: block;}.es-wrapper{width: 100%; height: 100%; background-image: ; background-repeat: repeat; background-position: center top;}.es-wrapper-color{background-color: #eeeeee;}.es-content-body{background-color: #ffffff;}.es-content-body p,.es-content-body ul li,.es-content-body ol li{color: #333333;}.es-content-body a{color: #ed8e20;}.es-header{background-color: transparent; background-image: ; background-repeat: repeat; background-position: center top;}.es-header-body{background-color: #044767;}.es-header-body p,.es-header-body ul li,.es-header-body ol li{color: #ffffff; font-size: 14px;}.es-header-body a{color: #ffffff; font-size: 14px;}.es-footer{background-color: transparent; background-image: ; background-repeat: repeat; background-position: center top;}.es-footer-body{background-color: #ffffff;}.es-footer-body p,.es-footer-body ul li,.es-footer-body ol li{color: #333333; font-size: 14px;}.es-footer-body a{color: #333333; font-size: 14px;}.es-infoblock,.es-infoblock p,.es-infoblock ul li,.es-infoblock ol li{line-height: 120%; font-size: 12px; color: #cccccc;}.es-infoblock a{font-size: 12px; color: #cccccc;}a.es-button{border-style: solid; border-color: #ed8e20; border-width: 15px 30px 15px 30px; display: inline-block; background: #ed8e20; border-radius: 5px; font-size: 16px; font-family: 'open sans ', 'helvetica neue ', helvetica, arial, sans-serif; font-weight: bold; font-style: normal; line-height: 120%; color: #ffffff; text-decoration: none !important; width: auto; text-align: center;}.activat_btn:link, activat_btn:visited{background-color: #f44336; color: white; padding: 14px 25px; text-align: center; text-decoration: none; display: inline-block;}activat_btn:hover, activat_btn:active{background-color: red;}.es-button-border{border-style: solid solid solid solid; border-color: transparent transparent transparent transparent; background: #ed8e20; border-width: 0px 0px 0px 0px; display: inline-block; border-radius: 5px; width: auto;}/* RESPONSIVE STYLES Please do not delete and edit CSS styles below. If you don't need responsive layout, please delete this section. */@media only screen and (max-width: 600px){p, ul li, ol li, a{font-size: 16px !important;}h1{font-size: 32px !important; text-align: center;}h2{font-size: 26px !important; text-align: center;}h3{font-size: 20px !important; text-align: center;}h1 a{font-size: 32px !important;}h2 a{font-size: 26px !important;}h3 a{font-size: 20px !important;}.es-menu td a{font-size: 16px !important;}.es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a{font-size: 16px !important;}.es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a{font-size: 16px !important;}.es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a{font-size: 12px !important;}*[class='gmail-fix']{display: none !important;}.es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3{text-align: center !important;}.es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3{text-align: right !important;}.es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3{text-align: left !important;}.es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img{display: inline !important;}.es-button-border{display: inline-block !important;}.es-button{font-size: 16px !important; display: inline-block !important; border-width: 15px 30px 15px 30px !important;}.es-btn-fw{border-width: 10px 0px !important; text-align: center !important;}.es-adaptive table, .es-btn-fw, .es-btn-fw-brdr, .es-left, .es-right{width: 100% !important;}.es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header{width: 100% !important; max-width: 600px !important;}.es-adapt-td{display: block !important; width: 100% !important;}.adapt-img{width: 100% !important; height: auto !important;}.es-m-p0{padding: 0px !important;}.es-m-p0r{padding-right: 0px !important;}.es-m-p0l{padding-left: 0px !important;}.es-m-p0t{padding-top: 0px !important;}.es-m-p0b{padding-bottom: 0 !important;}.es-m-p20b{padding-bottom: 20px !important;}.es-mobile-hidden, .es-hidden{display: none !important;}.es-desk-hidden{display: table-row!important; width: auto!important; overflow: visible!important; float: none!important; max-height: inherit!important; line-height: inherit!important;}.es-desk-menu-hidden{display: table-cell!important;}table.es-table-not-adapt, .esd-block-html table{width: auto !important;}table.es-social{display: inline-block !important;}table.es-social td{display: inline-block !important;}}/* END RESPONSIVE STYLES */.es-p-default{padding-top: 20px; padding-right: 35px; padding-bottom: 0px; padding-left: 35px;}.es-p-all-default{padding: 0px;}</style> <body> <div class='es-wrapper-color'> <table class='es-wrapper' width='100%' cellspacing='0' cellpadding='0'> <tbody> <tr> <td class='esd-email-paddings' valign='top'> <table class='es-content esd-header-popover' cellspacing='0' cellpadding='0' align='center'> <tbody> <tr> <td class='esd-stripe' esd-custom-block-id='7954' align='center'> <table class='es-content-body' style='background-color: transparent;' width='600' cellspacing='0' cellpadding='0' align='center'> <tbody> </tbody> </table> </td></tr></tbody> </table> <table class='es-content' cellspacing='0' cellpadding='0' align='center'> <tbody> <tr> </tr><tr> <td class='esd-stripe' esd-custom-block-id='7681' align='center'> <table class='es-header-body' style='background-color: rgb(4, 71, 103);' width='600' cellspacing='0' cellpadding='0' bgcolor='#044767' align='center'> <tbody> <tr> <td class='esd-structure es-p35t es-p35b es-p35r es-p35l' align='left'> <table class='es-left' cellspacing='0' cellpadding='0' align='left'> <tbody> <tr> <td class='es-m-p0r es-m-p20b esd-container-frame' width='340' valign='top' align='center'> <table width='100%' cellspacing='0' cellpadding='0'> <tbody> <tr> <td class='esd-block-text es-m-txt-c' align='left'> <h1 style='color: #ffffff; line-height: 100%;'>PolosysBooks</h1> </td></tr></tbody> </table> </td></tr></tbody> </table> <table cellspacing='0' cellpadding='0' align='right'> <tbody> <tr class='es-hidden'> <td class='es-m-p20b esd-container-frame' esd-custom-block-id='7704' width='170' align='left'> <table width='100%' cellspacing='0' cellpadding='0'> <tbody> <tr> <td class='esd-block-spacer es-p5b' align='center'> <table width='100%' height='100%' cellspacing='0' cellpadding='0' border='0'> <tbody> <tr> <td style='border-bottom: 1px solid rgb(4, 71, 103); background: rgba(0, 0, 0, 0) none repeat scroll 0% 0%; height: 1px; width: 100%; margin: 0px;'></td></tr></tbody> </table> </td></tr><tr> <td> <table cellspacing='0' cellpadding='0' align='right'> <tbody> </tbody> </table> </td></tr><tr> <td align='left' class='esd-block-text'> <p> <br></p></td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> <table class='es-content' cellspacing='0' cellpadding='0' align='center'> <tbody> <tr> <td class='esd-stripe' align='center'> <table class='es-content-body' width='600' cellspacing='0' cellpadding='0' bgcolor='#ffffff' align='center'> <tbody> <tr> <td class='esd-structure es-p40t es-p35b es-p35r es-p35l' esd-custom-block-id='7685' style='background-color: rgb(247, 247, 247);' bgcolor='#f7f7f7' align='left'> <table width='100%' cellspacing='0' cellpadding='0'> <tbody> <tr> <td class='esd-container-frame' width='530' valign='top' align='center'> <table width='100%' cellspacing='0' cellpadding='0'> <tbody> <tr> <td class='esd-block-text es-p15b' align='center'> <h2 style='color: #333333;'>Welocome Polosybooks!</h2> </td></tr><tr> <td class='esd-block-text es-m-txt-l es-p20t' align='left'> <h3 style='font-size: 18px;'>Hello "+data['fullName']+",</h3> </td></tr><tr> <td class='esd-block-text es-p15t es-p10b' align='left'> <p style='font-size: 16px; color: #777777;'>Thank you for creating a polosysbooks account. Please click the link below to activate your account.</p></td></tr><tr> <td class='esd-block-button es-p25t es-p20b es-p10r es-p10l' align='center'> <span class='es-button-border' style='background: none 0% 0% repeat scroll rgb(237, 142, 32);'> <a href='http://localhost:4200/app/home' class='activat_btn' target='_blank' style='font-weight: normal; border-width: 15px 30px; background: rgb(237, 142, 32) none repeat scroll 0% 0%; border-color: rgb(237, 142, 32); color: rgb(255, 255, 255); font-size: 18px;'>Activate account</a> </span> </td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> <table class='es-footer' cellspacing='0' cellpadding='0' align='center'> <tbody> <tr> <td class='esd-stripe' esd-custom-block-id='7684' align='center'> <table class='es-footer-body' width='600' cellspacing='0' cellpadding='0' align='center'> <tbody> <tr> <td class='esd-structure es-p35t es-p40b es-p35r es-p35l' align='left'> <table width='100%' cellspacing='0' cellpadding='0'> <tbody> <tr> <td class='esd-container-frame' width='530' valign='top' align='center'> <table width='100%' cellspacing='0' cellpadding='0'> <tbody> <tr> <td class='esd-block-text es-m-txt-c es-p5b' esdev-links-color='#777777' align='left'> <p style='color: #777777;'>If the button does not work, Please try copying this URL in your browser's addressa bar:&nbsp; <a href='http://localhost:4200/app/home'>http://localhost:4200/app/home</a> </p></td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> <table class='esd-footer-popover es-content' cellspacing='0' cellpadding='0' align='center'> <tbody> <tr> <td class='esd-stripe' align='center'> <table class='es-content-body' style='background-color: transparent;' width='600' cellspacing='0' cellpadding='0' align='center'> <tbody> <tr> <td class='esd-structure es-p30t es-p30b es-p20r es-p20l' align='left'> <table width='100%' cellspacing='0' cellpadding='0'> <tbody> <tr> <td class='esd-container-frame' width='560' valign='top' align='center'> <table width='100%' cellspacing='0' cellpadding='0'> <tbody> <tr> <td align='center' class='esd-empty-container' style='display: none;'></td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> </div></body></html>"
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return True

