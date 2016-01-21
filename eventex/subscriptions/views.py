from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscription(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscription/subscription_form.html',
                      {'form': form})

    _send_email('Confirmação de Inscrição',
                settings.DEFAULT_FROM_EMAIL,
                form.cleaned_data['email'],
                'subscription/subscription_email.txt',
                form.cleaned_data)

    Subscription.objects.create(**form.cleaned_data)

    messages.success(request, 'Inscrição realizada com sucesso!')

    return HttpResponseRedirect('/inscricao/')


def new(request):
    return render(request, 'subscription/subscription_form.html',
                  {'form': SubscriptionForm()})


def _send_email(subject, from_, to, template_name, context):
        body = render_to_string(template_name, context)
        mail.send_mail(subject, body, from_, [from_, to])
