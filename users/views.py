from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

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