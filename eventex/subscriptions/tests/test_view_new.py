from django.core import mail
from django.shortcuts import resolve_url
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.response = self.client.get(resolve_url('subscriptions:new'))

    def test_get(self):
        """GET /inscricao/ must return status_code 200"""
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """GET /inscricao/ must use template subscription/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        tags = (
            ('<form', 1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1),
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """HTML must contain csrf_token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have SubscriptionForm"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscriptionsNewPostValid(TestCase):
    def setUp(self):
        data = {'name': 'Guilherme Hubner', 'cpf': '12345678901', 'phone': '31-99223847',
                'email': 'guilherme_hubner@msn.com'}
        self.response = self.client.post(resolve_url('subscriptions:new'), data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertRedirects(self.response, resolve_url('subscriptions:detail', 1))

    def test_send_subscribe_email(self):
        """Valid POST should send one email"""
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewPostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post(resolve_url('subscriptions:new'), {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """Invalid POST should use template subscription/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        """Context must have SubscriptionForm"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        """Form must have errors messages"""
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())

class TemplateRegressionTest(TestCase):
    def test_template_has_no_field_errors(self):
        invalid_data = dict(name='Guilherme Hübner', cpf='12345678901')
        response = self.client.post(resolve_url('subscriptions:new'), invalid_data)

        self.assertContains(response, '<ul class="errorlist nonfield">')
