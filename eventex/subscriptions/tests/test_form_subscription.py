from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = SubscriptionForm()
        expected = ['name', 'cpf', 'phone', 'email']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        """CPF must only accept digits"""
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_has_11_digits(self):
        """CPF must have 11 digits"""
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        """Name must be capitalized"""
        form = self.make_validated_form(name='GUILHERME hübner')
        self.assertEqual(form.cleaned_data['name'], 'Guilherme Hübner')

    def test_email_is_optional(self):
        """Email is optional"""
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        """Phone is optional"""
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_email_or_phone(self):
        """Email and Phone are optional, but one must be informed"""
        form = self.make_validated_form(phone='', email='')
        self.assertListEqual(list(form.errors), ['__all__'])

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()[field]
        self.assertEqual(errors[0].code, code)

    def make_validated_form(self, **kwargs):
        valid = dict(name='Guilherme Hubner', cpf='12345678901', phone='31-987888531',
                     email='guilherme_hubner@msn.com')

        data = dict(valid, **kwargs)

        form = SubscriptionForm(data)
        form.is_valid()

        return form
