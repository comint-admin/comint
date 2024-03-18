from django import forms
from .validations import CashboardValidators
from ..models import LoanRequest, LOCNegotiationRequest

class LOCNegotiationRequestForm(forms.ModelForm):
    class Meta:
        model = LOCNegotiationRequest
        fields = ['amount', 'term', 'interest_rate']  
        
    def __init__(self, *args, **kwargs):
        self.loan_request = kwargs.pop('loan_request', None)
        super().__init__(*args, **kwargs)
        self.fields['amount'].label = "Proposed Funding Amount ($USD)"
        self.fields['term'].label = "Term (In Months)"

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return CashboardValidators.validate_amount(amount, self.loan_request)

    def clean_term(self):
        term = self.cleaned_data.get('term')
        if term is not None and term < 0:
            raise forms.ValidationError('Term must be non-negative')
        if term is not None and term > 360:
            raise forms.ValidationError('Term must be less than 360 months')
        return term

    def clean_interest_rate(self):
        interest_rate = self.cleaned_data.get('interest_rate')
        if interest_rate is not None and interest_rate < 0:
            raise forms.ValidationError('Interest rate must be non-negative')
        return interest_rate

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['name', 'description', 'amount', 'term', 'interest_rate']

    def __init__(self, *args, **kwargs):
        super(LoanRequestForm, self).__init__(*args, **kwargs)
        # Updating labels
        self.fields['amount'].label = "Initial Amount ($USD)"
        self.fields['term'].label = "Term (In Months)"
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 2})  


    def clean_term(self):
        term = self.cleaned_data.get('term')
        if term is not None and term < 0:
            raise forms.ValidationError('Term must be non-negative')
        if term is not None and term > 360:
            raise forms.ValidationError('Term must less than 360 months')
        return term

    def clean_interest_rate(self):
        interest_rate = self.cleaned_data.get('interest_rate')
        if interest_rate is not None and interest_rate < 0:
            raise forms.ValidationError('Interest rate must be non-negative')
        return interest_rate

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return CashboardValidators.validate_amount(amount)