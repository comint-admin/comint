from django import forms
from ..models import LoanRequest

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['term', 'interest_rate', 'amount', 'name', 'description']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount > 5000:
            raise forms.ValidationError('Loan amount cannot exceed 5000 USD')
        return amount