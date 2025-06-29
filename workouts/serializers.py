from rest_framework import serializers
from .models import Workout, Exercise, Set

class SetSerializer(serializers.ModelSerializer):
    set_number = serializers.IntegerField(min_value=1)
    reps = serializers.IntegerField(min_value=0)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0)

    class Meta:
        model = Set
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ExerciseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    sets = SetSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class WorkoutSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    date = serializers.DateField()
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
