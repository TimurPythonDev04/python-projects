from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


class TaskAuthorizationTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='testpass123')
        self.bob = User.objects.create_user(username='bob', password='testpass123')
        self.task = Task.objects.create(
            title='Alice task',
            description='desc',
            owner=self.alice,
        )

    def test_create_without_authentication_is_forbidden(self):
        response = self.client.post(
            reverse('task_create'),
            {'title': 'New task', 'description': 'desc'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_as_authenticated_user_sets_owner(self):
        self.client.force_authenticate(user=self.alice)
        response = self.client.post(
            reverse('task_create'),
            {'title': 'New task', 'description': 'desc'},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.alice.id)

    def test_update_by_non_owner_is_forbidden(self):
        self.client.force_authenticate(user=self.bob)
        response = self.client.put(
            reverse('task_update', args=[self.task.pk]),
            {'title': 'hacked', 'description': 'hacked'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_by_non_owner_is_forbidden(self):
        self.client.force_authenticate(user=self.bob)
        response = self.client.delete(
            reverse('task_delete', args=[self.task.pk]),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_by_owner_succeeds(self):
        self.client.force_authenticate(user=self.alice)
        response = self.client.put(
            reverse('task_update', args=[self.task.pk]),
            {'title': 'edited', 'description': 'edited'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'edited')
