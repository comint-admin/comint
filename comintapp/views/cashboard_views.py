from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView

from comintapp.services import LoanService
from ..models import LOCNegotiationRequest, LineOfCredit, LoanRequest
from ..forms.cashboard_forms import LOCNegotiationRequestForm, LoanRequestForm
from django.views.generic import TemplateView
from ..decorators import profile_verified_required  
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from ..filters import LoanRequestFilter
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse

@method_decorator([profile_verified_required], name='dispatch')
class LoanRequestDetailView(DetailView):
    model = LoanRequest
    template_name = 'comintapp/loan_request_detail.html'
    context_object_name = 'loan_request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loan_request = self.get_object()
        user = self.request.user

        loan_service = LoanService(loan_request, user)

        # Prepare the negotiations map for the template
        context['loc_negotiations_map'] = loan_service.get_loc_negotiations_map()

        # Check if the user has an existing LOC with this loan request
        existing_loc = loan_service.get_user_loc()
        context['existing_loc'] = existing_loc

        if existing_loc:
            # User is a lender with an existing LOC; only show their negotiations
            context['user_negotiations'] = loan_service.get_negotiations_for_loc(existing_loc)
            context['show_warning'] = True
        else:
            # User can view all LOC negotiations if they are the borrower or have no LOCs
            context['show_warning'] = False
        
        return context
    
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

    def form_valid(self, form):
        loan_request = form.save(commit=False)
        loan_request.user = self.request.user  # Assign the user here
        loan_request.save()

        # After saving, self.object will have the loan request instance that was just created and saved
        self.object = loan_request

        # Now set the success_url to the loan request's detail page
        self.success_url = reverse('comintapp:loan_request_detail', kwargs={'pk': self.object.pk})

        return super(LoanRequestCreateView, self).form_valid(form)

@method_decorator([profile_verified_required], name='dispatch')
class MarketplaceView(ListView):
    model = LoanRequest
    template_name = 'comintapp/marketplace.html'
    paginate_by = 6  # Adjust the number of items per page as needed

    def get_queryset(self):
        qs = LoanRequest.objects.filter(status='OPEN').order_by('-created_at')
        return LoanRequestFilter(self.request.GET, queryset=qs).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = LoanRequestFilter(self.request.GET, queryset=self.queryset)
        return context

@method_decorator([profile_verified_required], name='dispatch')
class ManageLoanView(DetailView):
    model = LoanRequest
    template_name = 'comintapp/manage_loan.html'
    context_object_name = 'loan_request'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            messages.warning(request, "You are not allowed to manage that loan.")
            return redirect('comintapp:')  # Redirect to profile completion page
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loan_request = self.get_object()
        user = self.request.user
        
        loan_service = LoanService(loan_request, user)
        context['funding_info'] = loan_service.get_funding_info()
        context['loc_negotiations_map'] = loan_service.get_loc_negotiations_map()
        
        return context