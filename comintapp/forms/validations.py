from django import forms

class CashboardValidators:
    @staticmethod
    def validate_amount(amount, loan_request=None):
        # Check if amount exceeds the limit for a loan request
        if loan_request and amount > loan_request.amount:
            raise forms.ValidationError(f'Amount cannot exceed the original loan request amount of ${loan_request.amount}')
        # General validation for amount limits
        if amount is not None and amount > 5000:
            raise forms.ValidationError('Loan amount cannot exceed 5000 USD')
        elif amount is not None and amount < 10:
            raise forms.ValidationError('Loan amount cannot be less than 10 USD')
        elif amount is None:
            raise forms.ValidationError('Loan amount is required')
        return amount
