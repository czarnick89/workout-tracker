from django.contrib import admin
from .models import Workout, Exercise, Set

class SetInline(admin.TabularInline):
    model = Set
    extra = 1

class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'user', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ExerciseInline]

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'workout', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SetInline]

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'set_number', 'reps', 'weight', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')