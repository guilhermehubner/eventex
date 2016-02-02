from django.core import mail
from django.shortcuts import resolve_url
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = {'name': 'Guilherme Hubner', 'cpf': '12345678901', 'phone': '31-987888531',
                'email': 'guilherme_hubner@msn.com'}
        self.response = self.client.post(resolve_url('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        """Subscription email subject must be 'Confirmação de Inscrição'"""
        expect = 'Confirmação de Inscrição'
        self.assertEqual(self.email.subject, expect)

    def test_subscription_email_from(self):
        """Subscription email from must be 'contato@eventex.com.br'"""
        expect = 'eventex.testes@gmail.com'
        self.assertEqual(self.email.from_email, expect)

    def test_subscription_email_to(self):
        """Subscription email to must be 'guilherme_hubner@msn.com'"""
        expect = ['eventex.testes@gmail.com', 'guilherme_hubner@msn.com']
        self.assertEqual(self.email.to, expect)

    def test_subscription_email_body(self):
        """Subscription email body must have POST data"""
        contents = ['Guilherme Hubner',
                    '12345678901',
                    'guilherme_hubner@msn.com',
                    '31-987888531',
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
