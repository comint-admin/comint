from django.test import TestCase
from django.core.exceptions import ValidationError
from unittest.mock import patch  
from .models import ComintUser, LoanRequest, LineOfCredit, LOCNegotiationRequest, LOCConfirmation

class ComintUserModelTestCase(TestCase):
    def test_user_creation(self):
        user = ComintUser.objects.create(email='test@example.com')
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertIsNone(user.first_name)
        self.assertIsNone(user.last_name)
        self.assertIsNone(user.display_name)

class LoanRequestModelTestCase(TestCase):
    def test_loan_request_creation(self):
        user = ComintUser.objects.create(email='test@example.com')
        loan_request = LoanRequest.objects.create(
            user=user,
            term=12,
            interest_rate=5.0,
            amount=4000,
            name='Test Loan',
            description='Test description'
        )
        self.assertEqual(loan_request.user, user)
        self.assertEqual(loan_request.term, 12)
        self.assertEqual(loan_request.interest_rate, 5.0)
        self.assertEqual(loan_request.amount, 4000)
        self.assertEqual(loan_request.name, 'Test Loan')
        self.assertEqual(loan_request.description, 'Test description')

class LineOfCreditModelTestCase(TestCase):
    @patch('comintapp.models.LineOfCredit.save')  
    def test_line_of_credit_creation(self, mock_loc_save):
        user = ComintUser.objects.create(email='test@example.com')
        loan_request = LoanRequest.objects.create(
            user=user,
            term=12,
            interest_rate=5.0,
            amount=4000,
            name='Test Loan',
            description='Test description'
        )
        mock_loc_save.return_value = None  
        line_of_credit = LineOfCredit.objects.create(
            loan_request=loan_request,
            negotiator=user
        )
        self.assertEqual(line_of_credit.loan_request, loan_request)
        self.assertEqual(line_of_credit.negotiator, user)

class LOCNegotiationRequestModelTestCase(TestCase):
    @patch('comintapp.models.LineOfCredit.save')  
    @patch('comintapp.models.LOCNegotiationRequest.save')  
    def test_loc_negotiation_request_creation(self, mock_loc_save1, mock_loc_save2):
        user = ComintUser.objects.create(email='test@example.com')
        loan_request = LoanRequest.objects.create(
            user=user,
            term=12,
            interest_rate=5.0,
            amount=4000,
            name='Test Loan',
            description='Test description'
        )
        line_of_credit = LineOfCredit.objects.create(
            loan_request=loan_request,
            negotiator=user
        )
        mock_loc_save1.return_value = None  
        mock_loc_save2.return_value = None  
        loc_negotiation_request = LOCNegotiationRequest.objects.create(
            line_of_credit=line_of_credit,
            request_creator=user,
            term=12,
            interest_rate=5.0,
            amount=3000
        )
        self.assertEqual(loc_negotiation_request.line_of_credit, line_of_credit)
        self.assertEqual(loc_negotiation_request.request_creator, user)
        self.assertEqual(loc_negotiation_request.term, 12)
        self.assertEqual(loc_negotiation_request.interest_rate, 5.0)
        self.assertEqual(loc_negotiation_request.amount, 3000)

class LOCConfirmationModelTestCase(TestCase):
    @patch('comintapp.models.LineOfCredit.save')
    @patch('comintapp.models.LOCConfirmation.save')
    @patch('comintapp.models.LOCNegotiationRequest.save')
    def test_loc_confirmation_creation(self, mock_loc_negotiation_save, mock_loc_confirmation_save, mock_loc_save):
        user = ComintUser.objects.create(email='test@example.com')
        loan_request = LoanRequest.objects.create(
            user=user,
            term=12,
            interest_rate=5.0,
            amount=4000,
            name='Test Loan',
            description='Test description'
        )
        line_of_credit = LineOfCredit.objects.create(
            loan_request=loan_request, 
            negotiator=user
        )
        mock_loc_save.return_value = None
        mock_loc_negotiation_save.return_value = None
        loc_negotiation_request = LOCNegotiationRequest.objects.create(
            line_of_credit=line_of_credit,
            request_creator=user,
            term=12,
            interest_rate=5.0,
            amount=3000
        )
        mock_loc_confirmation_save.return_value = None
        loc_confirmation = LOCConfirmation.objects.create(
            loc_negotiation_request=loc_negotiation_request,
            confirmed=True
        )
        self.assertEqual(loc_confirmation.loc_negotiation_request, loc_negotiation_request)
        self.assertTrue(loc_confirmation.confirmed)
