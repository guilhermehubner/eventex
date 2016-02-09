from django.test import TestCase
from django.shortcuts import resolve_url
from eventex.core.models import Speaker

class SpeakerDetailGet(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Grace Hopper',
            slug='grace-hopper',
            photo='http://hbn.link/hopper-pic',
            website='http://hbn.link/hopper-site',
            description='Programadora e Almirante'
        )

        self.response = self.client.get(resolve_url('speaker_detail', slug='grace-hopper'))

    def test_get(self):
        """GET should return status_code 200 """
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/speaker_detail.html')

    def test_html(self):
        contents = [
            'Grace Hopper',
            'Programadora e Almirante',
            'http://hbn.link/hopper-pic',
            'http://hbn.link/hopper-site'
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected)

    def test_context(self):
        """Speaker must be in context"""
        speaker = self.response.context['speaker']
        self.assertIsInstance(speaker, Speaker)


class SpeakerDetailNotFound(TestCase):
    def test_not_found(self):
        response = self.client.get(resolve_url('speaker_detail', slug='not-found'))
        self.assertEqual(response.status_code, 404)
