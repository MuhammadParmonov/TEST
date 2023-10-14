from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse 
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponse("Siz allaqachon tizimga kirib bo'lgansiz!")
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return HttpResponse("Username yoki Parol noto'g'ri")
    
    return render(request, "users/login.html")

def logout_view(request):
    if request.user.is_authenticated:
        if request.method =="POST":
            logout(request)
            return redirect("index")
        return render(request, "users/logout.html")
    else:
        return HttpResponse("Siz allaqachon tizimdan chiqib ketib bo'lgansiz!")
    
def signup_view(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        first_name = request.POST['first_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        has_error = False
        
        if User.objects.filter(email=email):
            messages.error(request, "Ushbu emsil bilan foydalanuvchi mmavjud!")
            has_error=True
        if User.objects.filter(username=username):
            messages.error(request, "Ushbu user name bilan foydalanuvchi mavjud!")
            has_error=True
        if password1 != password2:
            messages.error(request, "Parollar o'zaro mos emas!") 
            has_error=True
        if len(password1) < 8:
            messages.error(request, "Parol 8ta harakterdan iborat bo'lishi kerak!")
            has_error=True 
            
        if not has_error:
            user = User.objects.create(email=email, username=username, first_name=first_name)
            user.set_password(password1)
            user.save()
            return redirect('login')
        else:
            pass
    return render(request, "users/signup.html")