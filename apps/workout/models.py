from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)

class WorkoutManager(models.Manager):
    def trainerLoginValidation(self, form):
        errors = []
        try:
            trainer = self.get(email=form['email'])
            if not bcrypt.checkpw(form['password'].encode(),trainer.password.encode()):
                errors.append("Incorrect Email or ")
        except:
            errors.append("Incorrect Email or Password")
        if len(errors)>0:
            return False
        return True

    def trainerRegisterValidation(self, form):
        errors = []
        if len(form['fname'])<1:
            errors.append("Trainer's First name is required")
        if len(form['lname'])<1:
            errors.append("Trainer's Last name is required")
        if not EMAIL_REGEX.match(form['email']):
            errors.append("Must be a valid email")
        email_list = self.filter(email=form['email'])
        if len(email_list)>0:
            errors.append("Email already in use")
        if len(form['address'])<1:
            errors.append("Address Required")
        if len(form['city'])<1:
            errors.append("City Required")
        if len(form['state'])<1:
            errors.append("State Required")
        if len(form['zip'])<1:
            errors.append("Zip Code Required")

        if len(form['pwd'])<5:
            errors.append("Password must be longer than 5 characters")
        if form['pwd'] != form['confirm_pwd']:
            errors.append('Password must match confirm password')
        return errors

    def createTrainer(self, form):
        pw_hash = bcrypt.hashpw(form['pwd'].encode(), bcrypt.gensalt())
        trainer = self.create(
            fname=form['fname'],
            lname=form['lname'],
            email=form['email'],
            address=form['address'],
            city=form['city'],
            state=form['state'],
            zip=form['zip'],
            password=pw_hash
        )
        return trainer

    def clientValidation(self, form):
        errors = []

        return errors

    def dayValidation(self, form):
        errors = []

        return errors

    def workoutValidation(self, form):
        errors = []

        return errors



class Trainer(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.IntegerField()
    objects = WorkoutManager()

class Client(models.Model):
    trainer = models.OneToOneField(Trainer, related_name='clients')
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip = models.IntegerField(blank=True)
    objects = WorkoutManager()


class Workout_Day(models.Model):
    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    client = models.ManyToManyField(Client, related_name='workout_day')
    objects = WorkoutManager()


class Workout(models.Model):
    workout_day = models.ManyToManyField(Workout_Day, related_name='workouts')
    body_part = models.CharField(max_length=255)
    muscle_group = models.CharField(max_length=255)
    name_of_workout = models.CharField(max_length=255)
    description = models.TextField()
    objects = WorkoutManager()


