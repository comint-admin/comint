from django.views.generic import TemplateView


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
