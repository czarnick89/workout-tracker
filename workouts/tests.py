from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from workouts.models import Workout, Exercise, Set
from datetime import date
from rest_framework.settings import api_settings
from django.utils import timezone
from datetime import timedelta

api_settings.DEFAULT_THROTTLE_CLASSES = []

User = get_user_model()

class WorkoutTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Sample workout data
        self.workout_data = {
            "date": "2024-01-01",
            "name": "Morning Workout",
            "notes": "Felt great!"
        }

    def test_create_workout(self):
        url = reverse('workout-list-create')
        response = self.client.post(url, self.workout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.workout_data['name'])
        self.assertEqual(response.data['notes'], self.workout_data['notes'])

    def test_get_workouts(self):
        # Create a workout first
        workout = Workout.objects.create(user=self.user, date=date.today(), name="Test Workout")
        url = reverse('workout-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # At least one workout present
        self.assertEqual(response.data[0]['id'], workout.id)

    def test_update_workout(self):
        workout = Workout.objects.create(user=self.user, date=date.today(), name="Old Name")
        url = reverse('workout-detail', args=[workout.id])
        updated_data = {
            "date": str(date.today()),
            "name": "Updated Workout",
            "notes": "Updated notes"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Workout")

    def test_delete_workout(self):
        workout = Workout.objects.create(user=self.user, date=date.today(), name="To be deleted")
        url = reverse('workout-detail', args=[workout.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ExerciseTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='exerciseuser', email='exercise@example.com', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a workout to attach exercises to
        self.workout = Workout.objects.create(user=self.user, date=date.today(), name="Exercise Workout")

        self.exercise_data = {
            "workout": self.workout.id,
            "name": "Push Ups"
        }

    def test_create_exercise(self):
        url = reverse('exercise-list-create')
        response = self.client.post(url, self.exercise_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.exercise_data['name'])
        self.assertEqual(response.data['workout'], self.workout.id)

    def test_get_exercises(self):
        exercise = Exercise.objects.create(workout=self.workout, name="Squats")
        url = reverse('exercise-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], exercise.id)

    def test_update_exercise(self):
        exercise = Exercise.objects.create(workout=self.workout, name="Old Exercise")
        url = reverse('exercise-detail', args=[exercise.id])
        updated_data = {
            "workout": self.workout.id,
            "name": "Updated Exercise"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Exercise")

    def test_delete_exercise(self):
        exercise = Exercise.objects.create(workout=self.workout, name="Delete Me")
        url = reverse('exercise-detail', args=[exercise.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='setuser', email='set@example.com', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.workout = Workout.objects.create(user=self.user, date=date.today(), name="Set Workout")
        self.exercise = Exercise.objects.create(workout=self.workout, name="Bench Press")

        self.set_data = {
            "exercise": self.exercise.id,
            "set_number": 1,
            "reps": 10,
            "weight": "50.00"
        }

    def test_create_set(self):
        url = reverse('set-list-create')
        response = self.client.post(url, self.set_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['set_number'], self.set_data['set_number'])
        self.assertEqual(response.data['reps'], self.set_data['reps'])
        self.assertEqual(response.data['weight'], self.set_data['weight'])

    def test_get_sets(self):
        s = Set.objects.create(exercise=self.exercise, set_number=1, reps=8, weight=40.00)
        url = reverse('set-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], s.id)

    def test_update_set(self):
        s = Set.objects.create(exercise=self.exercise, set_number=1, reps=8, weight=40.00)
        url = reverse('set-detail', args=[s.id])
        updated_data = {
            "exercise": self.exercise.id,
            "set_number": 1,
            "reps": 12,
            "weight": "45.00"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reps'], 12)
        self.assertEqual(response.data['weight'], "45.00")

    def test_delete_set(self):
        s = Set.objects.create(exercise=self.exercise, set_number=1, reps=8, weight=40.00)
        url = reverse('set-detail', args=[s.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

from rest_framework import status
from django.utils import timezone
from datetime import timedelta

class WorkoutValidationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='edgeuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_workout_missing_date(self):
        response = self.client.post('/api/workouts/', {'name': 'Test Workout'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = response.data.get('error', {}).get('message', {})
        self.assertIn('date', error_message)

    def test_create_workout_with_future_date(self):
        future_date = (timezone.now().date() + timedelta(days=30)).isoformat()
        response = self.client.post('/api/workouts/', {'date': future_date})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Acceptable unless you restrict future dates

    def test_create_workout_with_long_name(self):
        long_name = 'W' * 500
        response = self.client.post('/api/workouts/', {'date': '2023-01-01', 'name': long_name})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = response.data.get('error', {}).get('message', {})
        self.assertIn('name', error_message)


class ExerciseValidationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='edgeuser2', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.workout = Workout.objects.create(user=self.user, date='2023-01-01')

    def test_create_exercise_missing_name(self):
        response = self.client.post('/api/exercises/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = response.data.get('error', {}).get('message', {})
        self.assertIn('name', error_message)

    def test_create_exercise_with_long_name(self):
        long_name = 'N' * 300
        response = self.client.post('/api/exercises/', {'name': long_name})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = response.data.get('error', {}).get('message', {})
        self.assertIn('name', error_message)


class SetValidationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='edgeuser3', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.workout = Workout.objects.create(user=self.user, date='2023-01-01')
        self.exercise = Exercise.objects.create(workout=self.workout, name='Squats')

    def test_create_set_negative_reps(self):
        data = {
            'exercise': self.exercise.id,
            'set_number': 1,
            'reps': -5,
            'weight': 20
        }
        response = self.client.post('/api/sets/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = response.data.get('error', {}).get('message', {})
        self.assertIn('reps', error_message)

    def test_create_set_negative_weight(self):
        data = {
            'exercise': self.exercise.id,
            'set_number': 1,
            'reps': 10,
            'weight': -10
        }
        response = self.client.post('/api/sets/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = response.data.get('error', {}).get('message', {})
        self.assertIn('weight', error_message)

    def test_create_set_missing_fields(self):
        response = self.client.post('/api/sets/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = response.data.get('error', {}).get('message', {})
        self.assertIn('exercise', error_message)
        self.assertIn('set_number', error_message)
        self.assertIn('reps', error_message)
        self.assertIn('weight', error_message)
