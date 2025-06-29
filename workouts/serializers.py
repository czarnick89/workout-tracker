from rest_framework import serializers
from .models import Workout, Exercise, Set

class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ExerciseSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
