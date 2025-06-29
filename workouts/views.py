from rest_framework import generics, permissions
from .models import Workout, Exercise, Set
from .serializers import WorkoutSerializer, ExerciseSerializer, SetSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class WorkoutListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkoutRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

class ExerciseListCreateAPIView(ListCreateAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Exercises for workouts owned by the user only
        return Exercise.objects.filter(workout__user=self.request.user)

    def perform_create(self, serializer):
        workout = serializer.validated_data.get('workout')
        if workout.user != self.request.user:
            raise PermissionDenied("You do not own this workout.")
        serializer.save()

class ExerciseRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Restrict access to exercises belonging to the user's workouts
        return Exercise.objects.filter(workout__user=self.request.user)

class SetListCreateAPIView(ListCreateAPIView):
    serializer_class = SetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Sets for exercises belonging to the user's workouts only
        return Set.objects.filter(exercise__workout__user=self.request.user)

    def perform_create(self, serializer):
        exercise = serializer.validated_data.get('exercise')
        if exercise.workout.user != self.request.user:
            raise PermissionDenied("You do not own this exercise.")
        serializer.save()

class SetRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Set.objects.filter(exercise__workout__user=self.request.user)
