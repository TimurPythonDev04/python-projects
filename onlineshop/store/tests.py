from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Order


class OrderOwnershipTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass12345')
        self.user2 = User.objects.create_user(username='user2', password='pass12345')

        self.order1 = Order.objects.create(
            user=self.user1,
            name='User One',
            email='user1@example.com',
            address='Address 1',
        )
        self.order2 = Order.objects.create(
            user=self.user2,
            name='User Two',
            email='user2@example.com',
            address='Address 2',
        )

    def test_my_orders_shows_only_own_orders(self):
        self.client.login(username='user1', password='pass12345')
        response = self.client.get(reverse('my_orders'))

        orders_shown = list(response.context['orders'])
        self.assertIn(self.order1, orders_shown)
        self.assertNotIn(self.order2, orders_shown)

    def test_order_detail_returns_404_for_other_users_order(self):
        self.client.login(username='user1', password='pass12345')
        response = self.client.get(reverse('order_detail', args=[self.order2.pk]))

        self.assertEqual(response.status_code, 404)
