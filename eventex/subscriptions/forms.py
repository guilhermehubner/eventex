from django import forms
from django.core.exceptions import ValidationError
from eventex.subscriptions.models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'cpf', 'phone', 'email']

    def clean_name(self):
        name = self.cleaned_data['name']
        return ' '.join([w.capitalize() for w in name.split(' ')])

    def clean(self):
        self.cleaned_data = super().clean()

        if not self.cleaned_data.get('phone') and not self.cleaned_data.get('email'):
            raise ValidationError('Informe seu e-mail ou telefone.')

        return self.cleaned_data
