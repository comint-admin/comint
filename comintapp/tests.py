from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from .models import LoanRequest, LOCNegotiationRequest, LOCConfirmation
from .services import LoanService
from django.db import IntegrityError, transaction

UserModel = get_user_model()

class LoanNegotiationTestCase(TestCase):
    def setUp(self):
        # Create users
        self.borrower = UserModel.objects.create_user(email='borrower@example.com', password='testpass123')
        self.lender1 = UserModel.objects.create_user(email='lender1@example.com', password='testpass123')
        self.lender2 = UserModel.objects.create_user(email='lender2@example.com', password='testpass123')
        
        # Create a loan request by the borrower
        self.loan_request = LoanRequest.objects.create(
            user=self.borrower,
            term=12,
            interest_rate=5.0,
            amount=5000.00,
            name="Borrower's Loan",
            description="Need a loan for XYZ reasons"
        )

    def test_loan_negotiation_flow(self):
        # Lender 1 initiates a line of credit and adds a negotiation request
        loan_service_lender1 = LoanService(self.loan_request, self.lender1)
        with transaction.atomic():
            loan_service_lender1.add_negotiation_request(4000.00, 12, 4.5)
        
        # Attempting to add another negotiation by lender 1 should fail
        with self.assertRaises(PermissionDenied):
            with transaction.atomic():
                loan_service_lender1.add_negotiation_request(3900.00, 12, 4.25)
        
        # Borrower attempts to negotiate, which should also fail since it's not their turn
        loan_service_borrower = LoanService(self.loan_request, self.borrower)
        with self.assertRaises(PermissionDenied):
            with transaction.atomic():
                loan_service_borrower.add_negotiation_request(4100.00, 12, 4.75)

        # Lender 2 initiates a negotiation, which should be allowed
        loan_service_lender2 = LoanService(self.loan_request, self.lender2)
        with transaction.atomic():
            loan_service_lender2.add_negotiation_request(4200.00, 12, 4.6)

        # Borrower counters lender 2's negotiation, which should be allowed
        with transaction.atomic():
            loan_service_borrower.add_negotiation_request(4300.00, 12, 4.8)

        # Lender 1 tries to negotiate again, which should now be allowed
        with transaction.atomic():
            loan_service_lender1.add_negotiation_request(4400.00, 12, 4.9)

        # Borrower accepts the last negotiation from lender 1
        last_negotiation_id = LOCNegotiationRequest.objects.latest('id').id
        accepted_negotiation = loan_service_borrower.accept_negotiation(last_negotiation_id)
        
        # Confirm the accepted negotiation by lender 1
        loan_service_lender1.confirm_negotiation(accepted_negotiation.id, confirm=True)

        # Check the status of the last negotiation
        self.assertEqual(LOCNegotiationRequest.objects.latest('id').status, 'ACCEPTED')
        self.assertTrue(LOCConfirmation.objects.latest('id').confirmed)