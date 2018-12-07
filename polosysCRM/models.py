from django.db import models
import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
class Branch(models.Model) :
    BranchID = models.IntegerField(primary_key=True)
    BranchCode= models.CharField(max_length=50)
    BranchName = models.CharField(max_length=100)
    Remarks = models.CharField(max_length=200)
    
class Country(models.Model) :
    CountryID = models.IntegerField(primary_key=True)
    CountryCode= models.CharField(max_length=50)
    CountryName = models.CharField(max_length=100)
    TimeZone = models.CharField(max_length=500)
    Remarks = models.CharField(max_length=200)
class Customers(models.Model) :
    CustomerID = models.IntegerField(primary_key=True)
    BranchID =  models.ForeignKey(Branch,on_delete=models.DO_NOTHING,null=False)
    CustomerFName = models.CharField(max_length=100)
    CustomerLName = models.CharField(max_length=100)
    CountryID = models.ForeignKey(Country,on_delete=models.DO_NOTHING,null=False)
    Address1 = models.CharField(max_length=100)
    Address2 = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    FirstLoggedDate = models.DateTimeField()
    ExpiryDate = models.DateTimeField()
    RenewalDate = models.DateTimeField()
    CreatedDate = models.DateTimeField()   
class Products(models.Model) :
    ProductID = models.IntegerField(primary_key=True)
    BranchID =  models.ForeignKey(Branch,on_delete=models.DO_NOTHING,null=False)
    ProductName= models.CharField(max_length=100)
    Remarks = models.CharField(max_length=200) 
    CreatedDate = models.DateTimeField()
class Users(AbstractBaseUser, PermissionsMixin) :
    UserID= models.IntegerField(primary_key=True)
    BranchID =  models.ForeignKey(Branch,on_delete=models.DO_NOTHING,null=False)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.CharField(db_index=True, unique=True,max_length=255)
    password = models.CharField(max_length=100)
    CustomerID= models.ForeignKey(Customers,on_delete=models.DO_NOTHING,null=False)
    ProductID= models.ForeignKey(Products,on_delete=models.DO_NOTHING,null=False)
    FirstLoggedDate = models.DateTimeField()
    ExpiryDate = models.DateTimeField()
    CreatedDate = models.DateTimeField()    
    IsActive = models.BooleanField(default=True) 
    IsAdmin = models.BooleanField(default=True) 
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    is_superuser = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['CustomerID']
    # is_anonymous = False
    # is_authenticated = False
    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
class RenewalDetails(models.Model) :
    RenewalDetailID = models.IntegerField(primary_key=True)
    BranchID =  models.ForeignKey(Branch,on_delete=models.DO_NOTHING,null=False)
    CustomerID = models.ForeignKey(Customers,on_delete=models.DO_NOTHING,null=False)
    ProductID = models.ForeignKey(Products,on_delete=models.DO_NOTHING,null=False)
    NoOfUsers = models.IntegerField()
    RenewalDate = models.DateTimeField()
    RenewalPeriodFrom  = models.DateTimeField()
    RenewalPeriodTo = models.DateTimeField()   
class RenewalUsers(models.Model) :
    RenewalUsersID = models.IntegerField(primary_key=True)
    BranchID =  models.ForeignKey(Branch,on_delete=models.DO_NOTHING,null=False)
    CustomerID = models.ForeignKey(Customers,on_delete=models.DO_NOTHING,null=False)
    ProductID = models.ForeignKey(Products,on_delete=models.DO_NOTHING,null=False)
    UserID= models.ForeignKey(Users,on_delete=models.DO_NOTHING,null=False)
    RenewalDetailID= models.ForeignKey(RenewalDetails,on_delete=models.DO_NOTHING,null=False)
class UserLoggedDetails(models.Model) :
    UserLoggedDetailID = models.IntegerField(primary_key=True)
    BranchID =  models.ForeignKey(Branch,on_delete=models.DO_NOTHING,null=False)
    UserID= models.ForeignKey(Users,on_delete=models.DO_NOTHING,null=False)
    MACAddress= models.CharField(max_length=100)
    IPAddress= models.CharField(max_length=100)
    Logindatetime = models.DateTimeField()
    Logoutdatatime = models.DateTimeField()   
class DatabaseInfo(models.Model):
    DatabaseInfoID = models.AutoField(primary_key=True)
    CustomerID = models.ForeignKey(Customers,on_delete=models.DO_NOTHING,null=False)
    ProductID= models.ForeignKey(Products,on_delete=models.DO_NOTHING,null=False)
    DatabaseName = models.CharField(max_length=100)
    Host = models.CharField(max_length=200)
    Port = models.IntegerField()
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)