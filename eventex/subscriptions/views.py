from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm


def subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            mail.send_mail('Confirmação de Inscrição',
                           render_to_string('subscription/subscription_email.txt', form.cleaned_data),
                           'contato@eventex.com.br',
                           ['contato@eventex.com.br', form.cleaned_data['email']])

            messages.success(request, 'Inscrição realizada com sucesso!')

            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscription/subscription_form.html',
                          {'form': form})

    context = {'form': SubscriptionForm()}
    return render(request, 'subscription/subscription_form.html', context)
