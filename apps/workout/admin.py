from django.contrib import admin
from .models import Trainer, Client, Workout_Day, Workout
# Register your models here.

admin.site.register(Trainer)
admin.site.register(Workout_Day)
admin.site.register(Client)
admin.site.register(Workout)
