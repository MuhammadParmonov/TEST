from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Test 
from .forms import TestFrom, QuestionForm

@login_required(login_url="login")
def index(request):
    tests = Test.objects.all()
    return render(request, "index.html", {'tests': tests})

@login_required(login_url="login")
def my_tests(request):
    tests = Test.objects.filter(author=request.user)
    form = QuestionForm()
    return render(request, "my_tests.html", {"form":form, "tests":tests})

@login_required(login_url="login")
def create_test(request):
    form = TestFrom()
    if request.method == "POST":
        form = TestFrom(data=request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.author = request.user
            form.save(commit=True)
            return redirect("index")
        else:
            return render(request, "create_test.html", {"form":form})
    return render(request, "create_test.html", {"form":form})

def create_question(request, test_id):
    test = Test.objects.get(id=test_id)
    form = QuestionForm()
    
    if request.method == "POST":
        add_again = request.POST.get("add-again")
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            form.save(commit=True)
            if add_again == "on":
                return redirect("create_question", test.id)
            else:
                return redirect("my_tests")
        else:
            return render(request, "create_question.html", {"form":form, "test":test})
    return render(request, "create_question.html", {"form":form, "test":test})

def update_test(request, test_id):
    test = Test.objects.get(id=test_id)
    form = TestFrom(instance=test)
    if request.method == "POST":
        form = TestFrom(instance=test, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("my_tests")
        else:
            return render(request, "update_test.html", {"form":form, "test":test})
    return render(request, "update_test.html", {"form":form, "test":test})