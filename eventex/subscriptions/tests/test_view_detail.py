from django.test import TestCase
from eventex.subscriptions.models import Subscription


class  SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(name='Guilherme Hübner',
                                          cpf='12345678901',
                                          email='guilherme_hubner@msn.com',
                                          phone='31-987888531')

        self.response = self.client.get('/inscricao/{}/'.format(self.obj.pk))

    def test_get(self):
        self.assertEquals(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_detail.html')

    def test_context(self):
        subscription = self.response.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = [self.obj.name,
                    self.obj.cpf,
                    self.obj.email,
                    self.obj.phone]

        with self.subTest():
            for expected in contents:
                self.assertContains(self.response, expected)


class SubscriptionDetailNotFound(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/0/')

    def test_not_found(self):
        self.assertEquals(self.response.status_code, 404)
