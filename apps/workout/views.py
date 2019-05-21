from django.shortcuts import render, redirect
from django.contrib import messages         #imports flash messages
from .models import *

# Create your views here.
def index(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'workout/home.html', context)

def login(request):
    context = {
        'title': 'Login',
    }
    return render(request, 'workout/login.html')

def register(request):
    context = {
        'title': 'Register',
    }
    return render(request, 'workout/register.html')

def login_verify(request):
    print(request.POST)
    if request.method =="POST":
        print('*'*50)
        print(request.POST)
    return redirect('/index')

def register_verify(request):
    print(request.POST)
    if request.method =="POST":
        print('*'*50)
        print(request.POST)
    return redirect('/index')