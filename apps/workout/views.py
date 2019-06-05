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
        'created_client': False,

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

def client_edit_verify(request):
    if request.method=='POST':

        try:
            client = Client.objects.filter(id = request.POST['id'])
        except ValueError:
            return redirect('/create_client_form')
        errors = Client.objects.clientValidation(request.POST, True)

        if errors and errors:
            for error in errors:
                messages.error(request, error)
        else:
            if len(client)==1:
                print(client[0].email)
                Client.objects.filter(id=request.POST['id']).update(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    phone=request.POST['phone'],
                    email=request.POST['email'],
                    address=request.POST['address'],
                    city=request.POST['city'],
                    state=request.POST['state'],
                    zip=request.POST['zip'],
                )

            return redirect('/client_search')
    # messages.info(request,'Error in processing Client Update')
    client = Client.objects.get(id=request.POST['id'])
    context = {
    'title': "Edit Client",
    'client':client,
    }
    # messages.info(request, 'Error in processing Client Update')
    return render(request, 'workout/edit_client.html', context)


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
            'title': 'Client Search',
        }
        return render(request, 'workout/client_search.html', context)

def all_clients_search(request):
    client = Client.objects.all()
    context = {
        'client':client,
        'title': 'Client Search',
    }
    return render(request, 'workout/client_search.html', context)


def edit_client(request, client_id):            #shows client to edit
    client = Client.objects.get(id= client_id)
    context = {
        'title': "Edit Client",
        'client':client,
    }
    return render(request, 'workout/edit_client.html', context)

def delete_client(request, client_id):
    del_client = Client.objects.get(id=client_id)
    del_name = del_client.fname +' ' +  del_client.lname
    del_client.delete()
    errors=[]
    errors.append(f'{del_name} was deleted')
    if errors and errors:
        for error in errors:
            messages.error(request, error)
    context = {
        'title': 'Client Search',
    }
    return render(request, 'workout/client_search.html', context)


# ---------Workout----------------
def create_workout(request, client_id):
    context = {
        'title': 'Create Workout'
    }
    return render(request, 'workout/create_workout.html', context)


def workout_search_form(request):
    context = {
        'title': 'Workout Search'
    }
    return render(request, 'workout/workout_search.html', context)

def workout_search(request):
    if request.method!="POST":
        return redirect('/workout_search_form')
    context = {
        'workout' : 'workouts'
    }
    if request.POST['name_of_workout']:
        wname = Workout.objects.filter(name_of_workout__startswith=request.POST['name_of_workout'])
        context = {
            'workout': wname
        }
        return render(request, 'workout/workout_search.html', context)
    if request.POST['muscle_group']:
        mg = Workout.objects.filter(muscle_group__startswith=request.POST['muscle_group'])
        context = {
            'workout': mg
        }
        print('In Muscle group')
        print(mg)
        return render(request, 'workout/workout_search.html', context)
    if request.POST['body_part']:
        bp = Workout.objects.filter(body_part__icontains=request.POST['body_part'].capitol())
        context = {
            'workout': bp
        }
        return render(request, 'workout/workout_search.html', context)
    return render(request, 'workout/workout_search.html', context)


def all_workout_search(request):
    pass

def workout_verify(request):
    pass

def edit_workout(request, id):
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

