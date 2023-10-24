from django.views.generic import FormView
from comintapp.forms.CaptchaForm import CaptchaForm


class CaptchaView(FormView):
    template_name = 'comintapp/captcha.html'
    form_class = CaptchaForm
    success_url = '/captcha_success'

    def form_valid(self, form):
        return super().form_valid(form)
