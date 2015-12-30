from django import forms


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF')
    phone = forms.CharField(label='Telefone')
    email = forms.EmailField(label='Email')
