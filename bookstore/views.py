from django.shortcuts import render ,redirect
from django.http import HttpResponse

# Create your views here.


from .models import *  #to use all classes into models.py
from .forms import OrderForm,CreateNewUser ,CustomerForm #to access class OrderForm and class CreateNewUser in file form.py  
from django.forms import inlineformset_factory 
from django.contrib import messages #if there is error send message
from .filters import OrderFilter #to access file filters

from django.contrib.auth.forms import UserCreationForm   #for useing logging and register (creation user)
from django.contrib.auth import authenticate , login ,logout #to use login and  logout
from django.contrib.auth.decorators import login_required #to returen users in login page if he dont loged
from .decorators import notLoggedUsers ,allowedUsers ,forAminds   #if user not logged user 
from django.contrib.auth.models import Group 

import requests # to use recaptcha in register 
from django.conf import settings # to use the key captcha in side the settings.py



@login_required(login_url='login') #if you want open home should be login
# @allowedUsers(allowedGroups=['admin'])
@forAminds
def home(request) :
    customers = Customer.objects.all()
    orders = Order.objects.all()
    t_order = orders.count()
    p_order = orders.filter(status ='Pending').count()
    d_order = orders.filter(status ='Delivered').count()
    in_order = orders.filter(status ='in progress').count()
    out_order = orders.filter(status ='out of order').count()

    context = {'customers' : customers,
               'orders' : orders,
               't_order' : t_order, # total order
               'p_order' : p_order, # count Pending
               'd_order' : d_order, # count Delivered
               'in_order' : in_order, # count in progress
               'out_order' : out_order,# count out of order
               }
    return render(request,'bookstore/dashboard.html' ,context)

@login_required(login_url='login')
@forAminds
def books(request) :
    books = Book.objects.all() # include all object like id ,name ,author all content inside the table books
    return render(request,'bookstore/books.html',{'books': books})  #request for file book.html and modle database class Book 

@login_required(login_url='login')
def customer(request,pk) : #pk primary key like id 1,2,3,4,,5 .....
    customer = Customer.objects.get(id=pk) # get to return id = priamary key (pk) inside the site
    orders = customer.order_set.all()
    number_order = orders.count()

    searchFilter = OrderFilter(request.GET,queryset=orders) #for searching in table order
    orders = searchFilter.qs

    context = {'customer':customer,
               'myFilter':searchFilter,
               'orders':orders,
               'number_order':number_order,
               }
    return render(request,'bookstore/customer.html',context)

# def create(request) :
#     form = OrderForm()
#     if request.method == 'POST':
#         # print(request.POST)
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')

#     context = {'form':form}
#     return render(request ,'bookstore/my_order_form.html',context )

@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def create(request,pk) :
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('book','status'),extra=3)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
           formset.save()
        return redirect('/')

    context = {'formset':formset}
    return render(request ,'bookstore/my_order_form.html',context )


@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def update(request,pk) :
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'formset':form}
    return render(request ,'bookstore/my_order_form.html',context )

@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def delete(request,pk) :
    orders = Order.objects.get(id=pk)
    if request.method == 'POST' :
        orders.delete()
        return redirect('/')
    context = {'orders':orders}
    return render(request ,'bookstore/delete_form.html',context )
 

@notLoggedUsers #if user not logged user 
def register(request) :
    # if request.user.is_authenticated :
    #   return redirect("home")
    # else :
        form = CreateNewUser()
        if request.method == 'POST':
            form = CreateNewUser(request.POST)
            if form.is_valid() :
                recaptcha_response = request.POST.get("g-recaptcha-response")
                data  = {
                    'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY , # this comming from settings.py
                    'response' : recaptcha_response , #this comming from page html register.html 
                }
                r = requests.post('https://www.google.com/recaptcha/api/siteverify',data = data) #للتحقق في كوكل من اختيار الاشياء الصحيحة  هذا الموقع يرجع اما فشل او نجاح 
                result = r.json()#يجيب النتيجة 
                if result['success'] :
                  user = form.save()
                  username = form.cleaned_data.get('username')
                # group = Group.objects.get(name="customer") # رجعلي جدول الكوستمر من الكروب الموجود في قاعدة البيانات 
                # user.groups.add(group) # add user in customer ضيف اليوزر الى جدول الكروب في جدول اليوزرس جدول الكروب عنده ثنين جداول الاول ادمن والثاني كوستومر
                  messages.success(request , username + ' CreatedSuccessfully !')
                  return redirect('login')
                else :
                    messages.error(request, ' Invalid Recaptcha Please try again ')

        context = {'form' : form}
        return render(request ,'bookstore/register.html',context )


@notLoggedUsers #if user not logged user 
def userLogin(request) :
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request ,username=username ,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else :
                messages.info(request,' Credentioal error ')
        context = {}
        return render(request ,'bookstore/login.html',context )
    


def userlogout(request) :
    logout(request)
    return redirect('login')



@login_required(login_url='login')
@allowedUsers(allowedGroups=['customer'])
def userProfile(request) :
    orders =request.user.customer.order_set.all()
    t_order = orders.count()
    p_order = orders.filter(status ='Pending').count()
    d_order = orders.filter(status ='Delivered').count()
    in_order = orders.filter(status ='in progress').count()
    out_order = orders.filter(status ='out of order').count()

    context = {
               'orders' : orders,
               't_order' : t_order, # total order
               'p_order' : p_order, # count Pending
               'd_order' : d_order, # count Delivered
               'in_order' : in_order, # count in progress
               'out_order' : out_order,# count out of order
               }
    return render(request ,'bookstore/profile.html',context )
    




@login_required(login_url='login')
def ProfileInfo(request) :
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST': #if user press in to POST(submit)
        form = CustomerForm(request.POST,request.FILES,instance=customer) #pring information (requsert.POST(text)) and (request.FILES (images))
        if form.is_valid() :
            form.save()

    context = {'form':form}
    return render(request ,'bookstore/profile_info.html',context )
    