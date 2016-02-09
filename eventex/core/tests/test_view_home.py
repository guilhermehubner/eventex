from django.test import TestCase
from django.shortcuts import resolve_url


class HomeTest(TestCase):
    fixtures = ['keynotes.json']

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

    def test_speakers(self):
        """Must show keynote speakers"""
        contents = ['Grace Hopper',
                    'http://hbn.link/hopper-pic',
                    'href="{}"'.format(resolve_url('speaker_detail', slug='grace-hopper')),
                    'Alan Turing',
                    'http://hbn.link/turing-pic',
                    'href="{}"'.format(resolve_url('speaker_detail', slug='alan-turing'))
                    ]

        for content in contents:
            with self.subTest():
                self.assertContains(self.response, content)

    def test_speakers_link(self):
        expected = 'href="{}#speakers"'.format(resolve_url('home'))
        self.assertContains(self.response, expected)
