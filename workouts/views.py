from rest_framework import generics, permissions, filters
from .models import Workout, Exercise, Set
from .serializers import WorkoutSerializer, ExerciseSerializer, SetSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10              # Number of items per page (you can adjust)
    page_size_query_param = 'page_size'  # Allow client to override, optional
    max_page_size = 100         # Max limit for page_size query param

class WorkoutListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['date', 'name']  # You can filter by date or name
    ordering_fields = ['date', 'name', 'created_at']  # You can order by these
    ordering = ['-date']  # Default ordering

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).prefetch_related('exercises')

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
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    # Use only fields that exist on the Exercise model
    filterset_fields = ['name']
    ordering_fields = ['name']
    ordering = ['-id']

    def get_queryset(self):
        return Exercise.objects.filter(workout__user=self.request.user).select_related('workout')

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
        return Exercise.objects.filter(workout__user=self.request.user).select_related('workout').order_by('id')

class SetListCreateAPIView(ListCreateAPIView):
    serializer_class = SetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    # Only include fields that exist on the Set model
    filterset_fields = ['set_number', 'reps', 'weight']
    ordering_fields = ['set_number', 'reps', 'weight']
    ordering = ['-id']

    def get_queryset(self):
        return Set.objects.filter(exercise__workout__user=self.request.user).select_related('exercise', 'exercise__workout')

    def perform_create(self, serializer):
        exercise = serializer.validated_data.get('exercise')
        if exercise.workout.user != self.request.user:
            raise PermissionDenied("You do not own this exercise.")
        serializer.save()


class SetRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Set.objects.filter(exercise__workout__user=self.request.user).select_related('exercise', 'exercise__workout').order_by('id')
