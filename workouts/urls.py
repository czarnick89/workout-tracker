from django.urls import path
from .views import (
    WorkoutListCreateAPIView,
    WorkoutRetrieveUpdateDestroyAPIView,
    ExerciseListCreateAPIView,
    ExerciseRetrieveUpdateDestroyAPIView,
    SetListCreateAPIView,
    SetRetrieveUpdateDestroyAPIView,
    )

urlpatterns = [
    path('workouts/', WorkoutListCreateAPIView.as_view(), name='workout-list-create'),
    path('workouts/<int:pk>/', WorkoutRetrieveUpdateDestroyAPIView.as_view(), name='workout-detail'),
    path('exercises/', ExerciseListCreateAPIView.as_view(), name='exercise-list-create'),
    path('exercises/<int:pk>/', ExerciseRetrieveUpdateDestroyAPIView.as_view(), name='exercise-detail'),
    path('sets/', SetListCreateAPIView.as_view(), name='set-list-create'),
    path('sets/<int:pk>/', SetRetrieveUpdateDestroyAPIView.as_view(), name='set-detail'),
]
