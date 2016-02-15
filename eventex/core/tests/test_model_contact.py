from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Guilherme Hubner',
            slug='guilherme-hubner',
            photo='https://avatars0.githubusercontent.com/u/5081283?v=3&s=460'
        )

    def test_email(self):
        Contact.objects.create(speaker=self.speaker, kind=Contact.EMAIL,
                               value='guilherme_hubner@msn.com')

        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        Contact.objects.create(speaker=self.speaker, kind=Contact.PHONE,
                               value='31-98788-8531')

        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contact kind should be limited to E or P"""
        contact = Contact.objects.create(speaker=self.speaker, kind='A',
                                         value='B')

        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker, kind=Contact.EMAIL, value='guilherme_hubner@msn.com')
        self.assertEqual(str(contact), 'guilherme_hubner@msn.com')
