from django import forms
from django.core.exceptions import ValidationError


def validade_cpf(value):
    if not value.isdigit():
        raise ValidationError('CPF deve conter apenas números', 'digits')

    if len(value) != 11:
        raise ValidationError('CPF deve ter 11 números', 'length')


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF', validators=[validade_cpf])
    phone = forms.CharField(label='Telefone', required=False)
    email = forms.EmailField(label='Email', required=False)

    def clean_name(self):
        name = self.cleaned_data['name']
        return ' '.join([w.capitalize() for w in name.split(' ')])

    def clean(self):
        if not self.cleaned_data.get('phone') and not self.cleaned_data.get('email'):
            raise ValidationError('Informe seu e-mail ou telefone.')

        return self.cleaned_data
