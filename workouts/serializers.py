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

class NestedExerciseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    sets = SetSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'sets']  # no 'workout' field here

class ExerciseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    sets = SetSerializer(many=True, read_only=True)
    workout = serializers.PrimaryKeyRelatedField(queryset=Workout.objects.all())

    class Meta:
        model = Exercise
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    date = serializers.DateField()
    exercises = NestedExerciseSerializer(many=True, required=False)

    class Meta:
        model = Workout
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises', [])
        workout = Workout.objects.create(**validated_data)
        for exercise_data in exercises_data:
            Exercise.objects.create(workout=workout, **exercise_data)
        return workout

    def update(self, instance, validated_data):
        exercises_data = validated_data.pop('exercises', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        existing_exercises = {ex.id: ex for ex in instance.exercises.all()}
        sent_ids = []

        for exercise_data in exercises_data:
            ex_id = exercise_data.get('id', None)
            if ex_id and ex_id in existing_exercises:
                ex = existing_exercises[ex_id]
                for attr, value in exercise_data.items():
                    if attr != 'id':
                        setattr(ex, attr, value)
                ex.save()
                sent_ids.append(ex_id)
            else:
                Exercise.objects.create(workout=instance, **exercise_data)

        for ex_id in existing_exercises.keys():
            if ex_id not in sent_ids:
                existing_exercises[ex_id].delete()

        return instance
    


