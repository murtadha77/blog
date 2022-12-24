


from django.urls import path
from . import views

from django.contrib.auth import views as authViews 


urlpatterns = [
    path('' ,views.home ,name="home"),
    path('books/' ,views.books,name="books"),
    path('customer/<str:pk>' ,views.customer , name="customer"), # str = string , pk = primary key 
    # path('create/' ,views.create , name="create"),
    path('create/<str:pk>' ,views.create , name="create"),
    path('update/<str:pk>' ,views.update , name="update"),
    path('delete/<str:pk>' ,views.delete , name="delete"),
    path('register/' ,views.register , name="register"),
    path('login/' ,views.userLogin , name="login"),
    path('logout/' ,views.userlogout , name="logout"),
    path('user/' ,views.userProfile , name="user_profile"),
    path('profile/' ,views.ProfileInfo , name="profile_info"),



    path('reset_password/' ,authViews.PasswordResetView.as_view(template_name ="bookstore/password_reset.html" ), name="reset_password"),
    path('reset_password_send/' ,authViews.PasswordResetDoneView.as_view(template_name ="bookstore/password_reset_sent.html"), name="reset_password_done"),
    path('reset/<uidb64>/<token>/' ,authViews.PasswordResetConfirmView.as_view(template_name ="bookstore/password_reset_form.html"), name="reset_password_confirm"),
    path('reset_password_complete/' ,authViews.PasswordResetCompleteView.as_view(template_name ="bookstore/password_reset_done.html"), name="reset_password_complete"),
   
]
