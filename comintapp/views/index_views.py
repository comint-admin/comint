from django.views.generic import TemplateView
from django.shortcuts import render

class IndexView(TemplateView):
    template_name = 'comintapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Assuming 'first_name' is a field on your custom user model
            context['username'] = self.request.user.display_name if self.request.user.display_name else self.request.user.email
        else:
            context['username'] = 'User'
        return context

class TncView(TemplateView):
    template_name = 'comintapp/tnc.html'

    def get_context_data(self, **kwargs):
        context = super(TncView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Assuming 'first_name' is a field on your custom user model
            context['username'] = self.request.user.display_name if self.request.user.display_name else self.request.user.email
        else:
            context['username'] = 'User'
        return context

class PrivacyView(TemplateView):
    template_name = 'comintapp/privacy.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Assuming 'first_name' is a field on your custom user model
            context['username'] = self.request.user.display_name if self.request.user.display_name else self.request.user.email
        else:
            context['username'] = 'User'
        return context

def loanView(request):
    context = {}
    if request.user.is_authenticated:
        # Assuming 'first_name' is a field on your custom user model
        context['username'] = request.user.first_name if request.user.first_name else request.user.email
    else:
        context['username'] = 'User'
    return render(request, "comintapp/loans.html", context)

class AboutView(TemplateView):
    template_name = 'comintapp/about.html'

def handleRequest(request):
    context = {}
    return render(request, "comintapp/index.html", context)

def fundRequests(request):
    context = {}
    if request.user.is_authenticated:
        # Assuming 'first_name' is a field on your custom user model
        context['username'] = request.user.first_name if request.user.first_name else request.user.email
    else:
        context['username'] = 'User'
    return render(request, "comintapp/fund_requests.html", context)

def payments(request):
    context = {}
    if request.user.is_authenticated:
        # Assuming 'first_name' is a field on your custom user model
        context['username'] = request.user.first_name if request.user.first_name else request.user.email
    else:
        context['username'] = 'User'
    return render(request, "comintapp/payments.html", context)

class ContactView(TemplateView):
    template_name = 'comintapp/contact.html'
