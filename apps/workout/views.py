from django.shortcuts import render, redirect
from django.contrib import messages         #imports flash messages
from .models import *
import re

# Create your views here.
def index(request):
    my_template = 'workout/template.html'

    context = {
        'title': 'Intro',
    }
    if 'trainer_id' in request.session:
        trainer = Trainer.objects.get(id = request.session['trainer_id'])
        context.update({'trainer':trainer})
        return render(request, 'workout/logged_in_home.html', context)
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

# ---------Clients----------------
def create_client_form(request):
    if 'trainer_id' not in request.session:
        return redirect('/login')
    current_trainer = Trainer.objects.get(id = request.session['trainer_id'])
    context = {
        'trainers':current_trainer,
        'title': "Create Client",
        'created_client': False
    }
    return render(request, 'workout/create_client_form.html', context)

def client_verify(request):
    if request.method=='POST':
        errors = Client.objects.clientValidation(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            current_trainer = Trainer.objects.get(id=request.session['trainer_id'])
            created_client = Client.objects.createClient(request.POST, current_trainer)
            context = {
                'trainers': current_trainer,
                'title': "Create Client",
                'created_client': created_client
            }
            return render(request, 'workout/create_client_form.html', context)

    return redirect("/create_client_form")

def client_search(request):
    if 'trainer_id' in request.session:
        context = {
            'title': 'Client Search',
        }
        return render(request, 'workout/client_search.html', context)

def client_name_search(request):
    if request.method == "POST":
        stripped_name = request.POST['name'].strip()
        stripped_name = stripped_name.lower()
        alphabet_lower = re.compile('[a-z]')
        fname=''
        lname=''
        first = True
        last = False
        name_list = list(stripped_name)
        while name_list:
            try:
                ''' Searching to see if the clients input is all alphabetic and lower.
                if there is a space, first name is over and last name starts.
                '''
                if alphabet_lower.search(name_list[0]) and first:
                    fname = fname +name_list[0]
                    print(name_list.pop(0))
                else:
                    print(name_list.pop(0))
                    first=False
                    last = True
                if alphabet_lower.search(name_list[0]) and last:
                    lname = lname + name_list[0]

            except IndexError:
                break

            '''Query for any option. Both first and last name, all users with first name
            and all users with last name if. Last name is only searched if nothing is found 
            during the first name search.'''
        if len(fname)>=1 and len(lname)>=1:
            client = Client.objects.filter(fname=fname.capitalize(), lname=lname.capitalize())
            # print("In both", client)
        elif len(fname)>=1 and len(lname)==0:
            client = Client.objects.filter(fname=fname.capitalize())
            # print('in fname', client)
            if not client.exists():
                client = Client.objects.filter(lname=fname.capitalize())
                # print('lname', client)
        context = {
            'client':client,
        }
        return render(request, 'workout/client_search.html', context)

def all_clients_search(request):
    client = Client.objects.all()
    context = {
        'client':client,
    }
    return render(request, 'workout/client_search.html', context)


def edit_client(request):
    pass

def delete_client(request):
    pass

# ---------Workout----------------
def create_workout(request):
    context = {
        'title': 'Create Workout'
    }
    return render(request, 'workout/create_workout.html', context)


def workout_search(request):
    pass

def workout_verify(request):
    pass

def edit_workout(request):
    pass

def delete_workout(request):
    pass

# --------Programs---------------------
def create_program(request):
    context = {
        'title': 'Create Program'
    }
    return render(request, 'workout/create_workout.html', context)


def edit_program(request):
    pass

def delete_program(request):
    pass




def logout(request):
    request.session.clear()
    return redirect('/index')