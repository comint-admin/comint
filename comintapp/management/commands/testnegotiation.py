# In your_app/management/commands/testnegotiations.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from comintapp.models import LoanRequest
from comintapp.services import LoanService

class Command(BaseCommand):
    help = 'Test the LoanService add_negotiation_request method'

    def handle(self, *args, **options):
        UserModel = get_user_model()
        borrower_email = 'borrower@example.com'  # Adjust as necessary
        lender_email = 'lender@example.com'  # Adjust as necessary

        # Fetch the borrower and lender users
        borrower = UserModel.objects.get(email=borrower_email)
        lender = UserModel.objects.get(email=lender_email)

        # Fetch the first LoanRequest object associated with the borrower
        loan_request = LoanRequest.objects.filter(user=borrower).first()
        if not loan_request:
            print("No loan request found for the borrower.")
            return

        loan_service_lender = LoanService(loan_request, lender)

        print(f"Lender ({lender.email}) is attempting to initiate a line of credit for the borrower's ({borrower.email}) loan request...")
        try:
            loan_service_lender.add_negotiation_request(amount=6000, term=12, interest_rate=5)
        except Exception as e:
            print(f"Operation failed: {e}")

        # Assuming the add_negotiation_request method takes care of creating or getting LOC
        # and also correctly handles transactions and validations
