from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionsTests(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscricao/ must return status_code 200"""
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """GET /inscricao/ must use template subscription/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscription/subscription_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """HTML must contain csrf_token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have SubscriptionForm"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'phone', 'email'], list(form.fields))


class SubscriptionsPostTests(TestCase):
    def setUp(self):
        data = {'name': 'Guilherme Hubner', 'cpf': '12345678901', 'phone': '31-99223847',
                'email': 'guilherme_hubner@msn.com'}
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(self.response.status_code, 302)

    def test_send_subscribe_email(self):
        """Valid POST should send one email"""
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        """Subscription email subject must be 'Confirmação de Inscrição'"""
        email = mail.outbox[0]
        expect = 'Confirmação de Inscrição'
        self.assertEqual(email.subject, expect)

    def test_subscription_email_from(self):
        """Subscription email from must be 'contato@eventex.com.br'"""
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'
        self.assertEqual(email.from_email, expect)

    def test_subscription_email_to(self):
        """Subscription email to must be 'guilherme_hubner@msn.com'"""
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'guilherme_hubner@msn.com']
        self.assertEqual(email.to, expect)

    def test_subscription_email_body(self):
        """Subscription email body must have POST data"""
        email = mail.outbox[0]
        self.assertIn('Guilherme Hubner', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('guilherme_hubner@msn.com', email.body)
        self.assertIn('31-99223847', email.body)

class SubscriptionsInvalidPost(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
         """Invalid POST should use template subscription/subscription_form.html"""
         self.assertTemplateUsed(self.response, 'subscription/subscription_form.html')

    def test_has_form(self):
        """Context must have SubscriptionForm"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        """Form must have errors messages"""
        form = self.response.context['form']
        self.assertTrue(form.errors)

class SubscriptionsSuccessMessage(TestCase):
    def setUp(self):
        data = {'name': 'Guilherme Hubner', 'cpf': '12345678901', 'phone': '31-99223847',
                'email': 'guilherme_hubner@msn.com'}
        self.response = self.client.post('/inscricao/', data, follow=True)

    def test_message(self):
        self.assertContains(self.response, 'Inscrição realizada com sucesso!')
