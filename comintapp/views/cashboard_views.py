from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from ..models import LoanRequest
from ..forms.cashboard_forms import LoanRequestForm
from django.views.generic import TemplateView
from ..decorators import profile_verified_required  
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

@method_decorator([login_required], name='dispatch')
class CashboardView(TemplateView):
    template_name = 'comintapp/cashboard.html'

@method_decorator([profile_verified_required], name='dispatch')
class LenderView(TemplateView):
    template_name = 'comintapp/lender_dashboard.html'

@method_decorator([profile_verified_required], name='dispatch')
class BorrowerView(TemplateView):
    template_name = 'comintapp/borrower_dashboard.html'


@method_decorator([profile_verified_required], name='dispatch')
class LoanRequestCreateView(CreateView):
    model = LoanRequest
    form_class = LoanRequestForm
    template_name = 'comintapp/create_loan_request.html'
    success_url = reverse_lazy('comintapp:cashboard')  # Redirect to a success page

    def form_valid(self, form):
        loan_request = form.save(commit=False)
        loan_request.user = self.request.user  # Assign the user here
        loan_request.save()
        return super().form_valid(form)

@method_decorator([profile_verified_required], name='dispatch')
class MarketplaceView(ListView):
    model = LoanRequest
    template_name = 'comintapp/marketplace.html'
    paginate_by = 2  # Adjust the number of items per page as needed

    def get_queryset(self):
        return LoanRequest.objects.filter(status='OPEN').order_by('-created_at')