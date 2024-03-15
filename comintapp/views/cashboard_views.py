from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the latest negotiation for this loan request
        latest_negotiation = LOCNegotiationRequest.objects.filter(
            line_of_credit__loan_request=self.object
        ).order_by('-created_at').first()

        # Determine if it's the loan creator's turn to respond
        context['is_creators_turn'] = latest_negotiation and latest_negotiation.status == 'COUNTERED'
        return context

    def get_queryset(self):
        # Ensure that only the loan creator can manage the loan
        return super().get_queryset().filter(user=self.request.user)
    
@method_decorator([login_required], name='dispatch')
class FundLoanView(FormView):
    template_name = 'comintapp/fund_loan.html'
    form_class = LOCNegotiationRequestForm
    success_url = reverse_lazy('comintapp:marketplace')

    def dispatch(self, request, *args, **kwargs):
        self.loan_request = get_object_or_404(LoanRequest, pk=self.kwargs['pk'])
        if self.request.user == self.loan_request.user:
            messages.warning(self.request, "You cannot fund your own loan request.")
            return redirect('comintapp:loan_request_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Find or create a LineOfCredit between the user and the loan request
        line_of_credit, created = LineOfCredit.objects.get_or_create(
            loan_request=self.loan_request,
            negotiator=self.request.user,
        )
        
        # Fetch the latest negotiation for the LOC between the user and the loan request
        latest_negotiation = LOCNegotiationRequest.objects.filter(
            line_of_credit__loan_request=self.loan_request,
            line_of_credit__negotiator=self.request.user
        ).order_by('-created_at').first()

        # Logic to check if it's user's turn to negotiate
        if latest_negotiation and latest_negotiation.status not in ['ACCEPTED', 'REJECTED', 'COUNTERED']:
            messages.error(self.request, "It's not your turn to negotiate.")
            return super().form_invalid(form)
        
        # Create LOC Negotiation Request
        negotiation_request = form.save(commit=False)
        negotiation_request.line_of_credit = line_of_credit
        negotiation_request.request_creator = self.request.user
        negotiation_request.save()
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loan_request'] = self.loan_request
        # Ensure we only show negotiations related to the current user's LOC
        line_of_credit = LineOfCredit.objects.filter(
            loan_request=self.loan_request, 
            negotiator=self.request.user
        ).first()
        
        if line_of_credit:
            context['negotiations'] = line_of_credit.negotiations.all().order_by('-created_at')
        else:
            context['negotiations'] = LOCNegotiationRequest.objects.none()
        
        # print(context['negotiations'])

        return context
