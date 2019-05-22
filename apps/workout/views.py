from django.shortcuts import render, redirect
from django.contrib import messages         #imports flash messages
from .models import *

# Create your views here.
def index(request):
    my_template = 'workout/template.html'

    context = {
        'title': 'Intro',
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
    if request.method =="POST" and Trainer.objects.trainerLoginValidation(request.POST):
        trainer = Trainer.objects.get(email=request.POST['email'])
        request.session['trainer_id'] = trainer.id
        print(request.session['trainer_id'])
        print('*'*50)
        return redirect('/index', request.session['trainer_id'])
    else:
        error = "Email or Password is invalid."
        messages.error(request, error)
        return redirect('/login')

def register_verify(request):
    print(request.method)
    print(request.POST['fname'])
    print('*'*50)
    if request.method =="POST":
        errors = Trainer.objects.trainerRegisterValidation(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            trainer = Trainer.objects.createTrainer(request.POST)
            request.session['trainer_id'] = trainer.id
            return redirect('/index')
    else:
        return redirect('/register')
    return redirect('/register')

def create_client(request):
    pass

def client_search(request):
    pass

def create_workout(request):
    pass

def workout_search(request):
    pass

def create_program(request):
    pass

def logout(request):
    request.session.clear()
    return redirect('/index')