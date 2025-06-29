from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    date = models.DateField()
    name = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name or 'Unnamed Workout'} - {self.date} ({self.user.username})"


class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Set(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='sets')
    set_number = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.exercise.name} – Set {self.set_number}: Reps {self.reps} @ {self.weight}"
