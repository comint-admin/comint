from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from ..models import LoanRequest
from ..forms.cashboard_forms import LoanRequestForm
from django.views.generic import TemplateView

class CashboardView(TemplateView):
    template_name = 'comintapp/cashboard.html'

class LenderView(TemplateView):
    template_name = 'comintapp/lender_dashboard.html'

class BorrowerView(TemplateView):
    template_name = 'comintapp/borrower_dashboard.html'


class LoanRequestCreateView(CreateView):
    model = LoanRequest
    form_class = LoanRequestForm
    template_name = 'comintapp/create_loan_request.html'
    success_url = reverse_lazy('success_page')  # Redirect to a success page

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assuming the user is logged in
        return super().form_valid(form)
