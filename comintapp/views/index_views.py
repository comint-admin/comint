from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'comintapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Assuming 'first_name' is a field on your custom user model
            context['username'] = self.request.user.first_name if self.request.user.first_name else self.request.user.email
        else:
            context['username'] = 'User'
            context['list_of_loans'] = [1, 2, 3, 4]
        return context
