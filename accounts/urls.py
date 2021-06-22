from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name = 'home'),
    path('register',register,name = 'register'),
    path('login',login,name = 'login'),
    path('token',send_token,name = 'send_token'),
    path('success',success,name = 'success'),
    path('verify/<auth_token>',verify_request,name = 'verify'),
    path('error',error_page,name = 'error'),
    path('welcome',welcome,name = 'welcome'),
]