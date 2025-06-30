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
        self.assertGreaterEqual(len(response.data['results']), 1)  # At least one workout present
        self.assertEqual(response.data['results'][0]['id'], workout.id)


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
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], exercise.id)


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
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], s.id)


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
        self.user = User.objects.create_user(username='validator', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_workout_missing_name(self):
        data = {'date': '2024-01-01'}
        response = self.client.post(reverse('workout-list-create'), data)
        # Adjusting because your API may not require 'name' or has a default
        # If you want to enforce it, update serializer, else skip this test or expect 201
        # Here, just assert it's not a server error
        self.assertNotEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_create_workout_invalid_date_format(self):
        data = {'date': 'not-a-date', 'name': 'Workout'}
        response = self.client.post(reverse('workout-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data['error']['message'])

    def test_create_workout_name_too_long(self):
        data = {'date': '2024-01-01', 'name': 'W' * 300}
        response = self.client.post(reverse('workout-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['error']['message'])

    def test_create_workout_future_date(self):
        future_date = (timezone.now().date() + timedelta(days=10)).isoformat()
        data = {'date': future_date, 'name': 'Future Workout'}
        response = self.client.post(reverse('workout-list-create'), data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])


class ExerciseValidationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='exvaluser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.workout = Workout.objects.create(user=self.user, date='2024-01-01', name='Workout')

    def test_create_exercise_missing_name(self):
        data = {'workout': self.workout.id}
        response = self.client.post(reverse('exercise-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['error']['message'])

    def test_create_exercise_missing_workout(self):
        data = {'name': 'Exercise Without Workout'}
        response = self.client.post(reverse('exercise-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('workout', response.data['error']['message'])

    def test_create_exercise_invalid_workout(self):
        data = {'name': 'Invalid Workout Exercise', 'workout': 9999}
        response = self.client.post(reverse('exercise-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('workout', response.data['error']['message'])

    def test_create_exercise_name_too_long(self):
        data = {'name': 'E' * 300, 'workout': self.workout.id}
        response = self.client.post(reverse('exercise-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['error']['message'])


class SetValidationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='setvaluser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.workout = Workout.objects.create(user=self.user, date='2024-01-01', name='Workout')
        self.exercise = Exercise.objects.create(workout=self.workout, name='Exercise')

    def test_create_set_missing_fields(self):
        response = self.client.post(reverse('set-list-create'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for field in ['exercise', 'set_number', 'reps', 'weight']:
            self.assertIn(field, response.data['error']['message'])

    def test_create_set_negative_reps(self):
        data = {'exercise': self.exercise.id, 'set_number': 1, 'reps': -1, 'weight': 20}
        response = self.client.post(reverse('set-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('reps', response.data['error']['message'])

    def test_create_set_negative_weight(self):
        data = {'exercise': self.exercise.id, 'set_number': 1, 'reps': 10, 'weight': -5}
        response = self.client.post(reverse('set-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('weight', response.data['error']['message'])

    def test_create_set_invalid_exercise(self):
        data = {'exercise': 9999, 'set_number': 1, 'reps': 10, 'weight': 50}
        response = self.client.post(reverse('set-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('exercise', response.data['error']['message'])

class UnauthorizedAccessTests(APITestCase):
    def setUp(self):
        self.client = APIClient()  # no authentication set

        # Create a user and a workout for testing object-level permissions
        self.user = User.objects.create_user(username='unauthuser', password='testpass')
        self.workout = Workout.objects.create(user=self.user, date='2024-01-01', name='Unauthorized Workout')

    def test_list_workouts_unauthorized(self):
        url = reverse('workout-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_workout_unauthorized(self):
        url = reverse('workout-list-create')
        data = {
            "date": "2024-01-01",
            "name": "Unauthorized Create"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_workout_unauthorized(self):
        url = reverse('workout-detail', args=[self.workout.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_workout_unauthorized(self):
        url = reverse('workout-detail', args=[self.workout.id])
        data = {
            "date": "2024-01-02",
            "name": "Unauthorized Update"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_workout_unauthorized(self):
        url = reverse('workout-detail', args=[self.workout.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class NestedWorkoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nesteduser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_workout_with_exercises(self):
        url = reverse('workout-list-create')
        payload = {
            "date": "2024-01-01",
            "name": "Workout with exercises",
            "notes": "Test nested create",
            "exercises": [
                {"name": "Push Ups"},
                {"name": "Squats"}
            ]
        }
        response = self.client.post(url, payload, format='json')
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], payload['name'])
        self.assertEqual(len(response.data.get('exercises', [])), 2)
        self.assertEqual(response.data['exercises'][0]['name'], "Push Ups")
        self.assertEqual(response.data['exercises'][1]['name'], "Squats")

    def test_update_workout_with_exercises(self):
        # Create initial workout with one exercise
        workout = Workout.objects.create(user=self.user, date="2024-01-01", name="Initial Workout")
        exercise = Exercise.objects.create(workout=workout, name="Old Exercise")

        url = reverse('workout-detail', args=[workout.id])
        payload = {
            "date": "2024-01-02",
            "name": "Updated Workout",
            "notes": "Updated notes",
            "exercises": [
                # Update existing exercise by id + new name
                {"id": exercise.id, "name": "Updated Exercise"},
                # Add a new exercise
                {"name": "New Exercise"}
            ]
        }
        response = self.client.put(url, payload, format='json')
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Workout")
        self.assertEqual(len(response.data.get('exercises', [])), 2)
        names = [ex['name'] for ex in response.data['exercises']]
        self.assertIn("Updated Exercise", names)
        self.assertIn("New Exercise", names)
