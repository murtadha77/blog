from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

#table of customer
class Customer(models.Model) :
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE) #on_delete=True it means if you press
    name=models.CharField( max_length=190,null=True)
    email=models.CharField( max_length=190,null=True)
    phone=models.CharField( max_length=190,null=True)
    age=models.CharField( max_length=190,null=True)
    avatar = models.ImageField(blank=True,null=True,default="personal.png")
    date_create =models.DateTimeField(auto_now_add=True,null=True)


    def __str__(self) -> str: #to returen name 
        return self.name 

class Tag(models.Model) :
    name   =models.CharField( max_length=190,null=True)

    def __str__(self) :
        return self.name



#table of BOOK
class Book(models.Model) :
    CATEGORY = (                                #for choices 
        ('Classics','Classics') ,
        ('Crime','Crime') ,
        ('Fantasy','Fantasy') ,
        ('Adventure stories','Adventure stories') ,
        ('Horror ',' Horror') ,
    )
    name   =models.CharField( max_length=50,null=True)
    author =models.CharField( max_length=50,null=True)
    price  =models.FloatField( max_length=50,null=True)
    category=models.CharField( max_length=50,null=True,choices=CATEGORY)
    description =models.CharField( max_length=300,null=True)
    tag = models.ManyToManyField(Tag)
    date_create =models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self) :
        return self.name



#table of order 
class Order(models.Model) : 
    STATUS = (                                #for choices 
        ('Pending','Pending') ,
        ('Delivered','Delivered') ,
        ('in progress','in progress') ,
        ('out of order','out of order') ,
    )
    customers = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL) #one to many
    book = models.ForeignKey(Book,null=True,on_delete=models.SET_NULL)#one to many
    tag = models.ManyToManyField(Tag)    #many to many
    date_create =models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField( max_length=50,null=True,choices=STATUS)



