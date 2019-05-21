from django.db import models

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
    def trainerLoginValidation(self, postData):
        errors = {}
        if len(postData['email'])<1:
            errors['name'] = "Trainer's First name is required"
        if len(postData['lname'])<1:
            errors['name'] = "Trainer's Last name is required"

    def trainerValidation(self, postData):
        errors = {}
        if len(postData['fname'])<1:
            errors['name'] = "Trainer's First name is required"
        if len(postData['lname'])<1:
            errors['name'] = "Trainer's Last name is required"

        return errors

    def clientValidation(self, postData):
        errors = {}

        return errors

    def dayValidation(self, postData):
        errors = {}

        return errors

    def workoutValidation(self, postData):
        errors = {}

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


