from django.test import TestCase
from django.shortcuts import resolve_url


class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get(resolve_url('home'))

    def test_get(self):
        """GET / must return status_code 200 """
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """ GET / must use index.html """
        self.assertTemplateUsed(self.response, 'index.html')

    def test_subscription_link(self):
        expected = 'href="{}"'.format(resolve_url('subscriptions:new'))
        self.assertContains(self.response, expected)
