from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm
from django.shortcuts import get_object_or_404
from main.models import Test, CheckTest

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponse("Siz allaqachon tizimga kirib bo'lgansiz!")
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
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



@login_required(login_url="login")
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    profileForm = ProfileForm(instance=user.profile)
    if request.method == "POST":
        profileForm = ProfileForm(instance=user.profile, data=request.POST, files=request.FILES)
        form = UserForm(instance=user, data=request.POST)
        if form.is_valid() and profileForm.is_valid():
            form.save()
            profileForm.save()
            return redirect("profile", user.username)
        else:
            return render(request, "users/user_update.html", {"form":form, "profileForm":profileForm})                    
    return render(request, "users/user_update.html", {"form":form, "profileForm":profileForm})

def profile(request, username):
    # user = User.objects.get(id=user_id)
    user = get_object_or_404(User, username=username)
    if user.profile.anonym == False or user == request.user: 
        number_of_tests = Test.objects.filter(author=user).count()
        check_tests = CheckTest.objects.filter(student=user)
        number_of_checktests = check_tests.count()
        tests = []
        for checktest in check_tests:
            print(checktest)
            if not checktest.test in tests:
                tests.append(checktest.test)
        context = {
            "user": user,
            "number_of_tests": number_of_tests,
            "number_of_checktests": number_of_checktests,
            "tests": tests,
            "chekcktests": check_tests,
        }
        return render(request, 'users/profile.html', context)
    else:
        raise Http404("Bu ser anonym")