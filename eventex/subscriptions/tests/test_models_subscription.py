from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(
            name='Guilherme Hübner',
            cpf='12345678901',
            email='guilherme@hubner.com',
            phone='31-987888531'
        )

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEquals(str(self.obj), self.obj.name)

    def test_paid_default_to_False(self):
        """By default, paid must be false"""
        self.assertEqual(self.obj.paid, False)
