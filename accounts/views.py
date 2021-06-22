from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    return render(request , 'home.html')



def register(request):
    if request.method == "POST":
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                
                
                if User.objects.filter(username=username).first():
                    messages.success(request,"Username is already taken")
                    return redirect('/register')
                
                if User.objects.filter(email=email).first():
                    messages.success(request,"Email is already taken")
                    return redirect('/register')
                
                user_obj = User(username=username, email=email)
                user_obj.set_password(password)
                user_obj.save()
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user = user_obj,auth_token=auth_token)
                profile_obj.save()
                send_mail_after_registration(email, auth_token)
                return redirect('/token')
            except Exception as e:
                print(e)
    
    return render(request,'register.html')
def login(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username).first()

        if user_obj is None:
            messages.success(request,'User not found')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user = user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,"Your profile is not verified, check your mail settings")
            return redirect('/login')

        user = authenticate(username = username, password = password)
        if user is None:
            messages.success(request,"Welcome")
            return redirect('/')
        auth_login(request, user)
        return redirect('/welcome')
    return render(request,'login.html')

def success(request):
    return render(request,'success.html')

def send_token(request):
    return render(request,'send_token.html')

def send_mail_after_registration(email, token):
    subject = "Please verify your account"
    message = f'Paste the link to verify http://127.0.0.1:8000/verify/{token}'
    email_form = settings.EMAIL_HOST_USER
    recepient_list = [email]
    send_mail(subject, message,email_form,recepient_list)

def verify_request(request,auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,"Your email has been already verified")
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,"Your email has been verified")
            return redirect('/login')

        else:
            return redirect('/error')
    except Exception as e:
        print(e)

def error_page(request):
    return render(request,'error.html')

def welcome(request):
    return render(request,'welcome.html')
