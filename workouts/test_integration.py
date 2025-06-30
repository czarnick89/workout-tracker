from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from workouts.models import Workout

class UserFlowIntegrationTests(APITestCase):
    def test_register_login_crud_workout(self):
        # Register user
        register_url = reverse('register')
        user_data = {
            'username': 'integrationuser',
            'email': 'integrationuser@example.com',
            'password': 'StrongPass123!'
        }
        response = self.client.post(register_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Login user (get token)
        login_url = reverse('token_obtain_pair')
        login_data = {
            'username': 'integrationuser',
            'password': 'StrongPass123!'
        }
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access']

        # Set auth header for next requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Create a workout
        workout_list_create_url = reverse('workout-list-create')
        workout_data = {
            'date': '2023-06-29',
            'name': 'Integration Test Workout'
        }
        response = self.client.post(workout_list_create_url, workout_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        workout_id = response.data['id']

        # Retrieve the workout
        workout_detail_url = reverse('workout-detail', kwargs={'pk': workout_id})
        response = self.client.get(workout_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Integration Test Workout')

        # Update the workout
        updated_data = {
            'date': '2023-06-30',
            'name': 'Updated Integration Workout'
        }
        response = self.client.put(workout_detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Integration Workout')

        # Delete the workout
        response = self.client.delete(workout_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # ✅ Confirm deletion at the database level
        self.assertFalse(
            Workout.objects.filter(pk=workout_id).exists(),
            msg="Workout should be deleted from the database but still exists."
        )
