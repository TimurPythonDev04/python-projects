from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskAuthorizationTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='OwnerPass123!')
        self.other = User.objects.create_user(username='other', password='OtherPass123!')
        self.task = Task.objects.create(title='Owner task', user=self.owner)

        self.detail_url = reverse('task-detail', args=[self.task.pk])
        self.update_url = reverse('task-update', args=[self.task.pk])
        self.delete_url = reverse('task-delete', args=[self.task.pk])
        self.create_url = reverse('task-create')

    def assertRedirectsToLogin(self, response, next_url):
        self.assertRedirects(response, f"{reverse('login')}?next={next_url}")

    def test_anonymous_user_is_redirected_to_login_on_detail(self):
        response = self.client.get(self.detail_url)
        self.assertRedirectsToLogin(response, self.detail_url)

    def test_anonymous_user_is_redirected_to_login_on_update(self):
        response = self.client.get(self.update_url)
        self.assertRedirectsToLogin(response, self.update_url)

    def test_anonymous_user_is_redirected_to_login_on_delete(self):
        response = self.client.get(self.delete_url)
        self.assertRedirectsToLogin(response, self.delete_url)

    def test_anonymous_user_is_redirected_to_login_on_create_get(self):
        response = self.client.get(self.create_url)
        self.assertRedirectsToLogin(response, self.create_url)

    def test_anonymous_user_cannot_create_task_via_post(self):
        response = self.client.post(self.create_url, {'title': 'Should not be created'})
        self.assertRedirectsToLogin(response, self.create_url)
        self.assertFalse(Task.objects.filter(title='Should not be created').exists())

    def test_other_user_gets_404_on_detail(self):
        self.client.login(username='other', password='OtherPass123!')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 404)

    def test_other_user_gets_404_on_update(self):
        self.client.login(username='other', password='OtherPass123!')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 404)

    def test_other_user_gets_404_on_delete(self):
        self.client.login(username='other', password='OtherPass123!')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 404)

    def test_other_user_post_does_not_change_or_delete_task(self):
        self.client.login(username='other', password='OtherPass123!')
        self.client.post(self.update_url, {'title': 'Hijacked title'})
        self.client.post(self.delete_url)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Owner task')

    def test_owner_can_view_detail(self):
        self.client.login(username='owner', password='OwnerPass123!')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Owner task')

    def test_owner_can_update_task(self):
        self.client.login(username='owner', password='OwnerPass123!')
        response = self.client.post(self.update_url, {'title': 'Updated title'})
        self.assertRedirects(response, reverse('task-list'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated title')

    def test_owner_can_delete_task(self):
        self.client.login(username='owner', password='OwnerPass123!')
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, reverse('task-list'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())


class TaskCreateFormTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='OwnerPass123!')
        self.client.login(username='owner', password='OwnerPass123!')

    def test_create_task_with_valid_date_is_saved_and_owned_by_current_user(self):
        response = self.client.post(reverse('task-create'), {
            'title': 'Task with a date',
            'description': 'some description',
            'due_date': '2026-12-25T14:30',
        })
        self.assertRedirects(response, reverse('task-list'))

        task = Task.objects.get(title='Task with a date')
        self.assertEqual(task.user, self.owner)
        self.assertIsNotNone(task.due_date)


class TaskDetailViewSafetyTests(TestCase):
    def test_get_request_to_detail_does_not_delete_the_task(self):
        owner = User.objects.create_user(username='owner', password='OwnerPass123!')
        task = Task.objects.create(title='Should survive GET', user=owner)
        self.client.login(username='owner', password='OwnerPass123!')

        response = self.client.get(reverse('task-detail', args=[task.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
