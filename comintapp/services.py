from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from .models import ComintUser, LineOfCredit, LOCNegotiationRequest, LOCConfirmation

class LoanService:
    MAX_LOAN_AMOUNT = 5000
    MIN_LOAN_AMOUNT = 10
    
    def _validate_loan_amount(self, amount):
        if amount > self.MAX_LOAN_AMOUNT:
            raise ValidationError(f"Loan amount cannot exceed ${self.MAX_LOAN_AMOUNT}")
        if amount < self.MIN_LOAN_AMOUNT:
            raise ValidationError(f"Loan amount must be at least ${self.MIN_LOAN_AMOUNT}")

    def _validate_negotiation_amount(self, amount):
        self._validate_loan_amount(amount)
        if amount > self.loan_request.amount:
            raise ValidationError("Negotiation amount cannot exceed the original loan amount")
   
    def _validate_term(self, term):
        if term < 0:
            raise ValidationError('Term must be non-negative')
        if term > 360:
            raise ValidationError('Term must be less than 360 months')

    def _validate_interest_rate(self, interest_rate):
        if interest_rate < 0:
            raise ValidationError('Interest rate must be non-negative')


    def __init__(self, loan_request, user):
        self.loan_request = loan_request
        self.user = user
        self.is_borrower = self.loan_request.user == user
        self.is_lender = not self.is_borrower

    def create_or_get_loc(self):
        if self.is_borrower:
            raise PermissionDenied("Borrowers cannot fund their own loan requests.")
        loc, created = LineOfCredit.objects.get_or_create(
            loan_request=self.loan_request,
            negotiator=self.user
        )
        return loc, created

    def get_user_loc(self):
        # Returns the LOC for the current user and loan request if it exists
        return LineOfCredit.objects.filter(loan_request=self.loan_request, negotiator=self.user).first()

    def _get_last_negotiation(self, loc):
        return loc.negotiations.order_by('-created_at').first()

    def _can_negotiate(self, loc):
        last_negotiation = self._get_last_negotiation(loc)
        if not last_negotiation:
            return self.is_lender
        if last_negotiation.status in ['ACCEPTED', 'REJECTED', 'CANCELLED']:
            return False
        return last_negotiation.request_creator != self.user

    @transaction.atomic
    def add_negotiation_request(self, amount, term, interest_rate):
        
        self._validate_loan_amount(amount)
        self._validate_negotiation_amount(amount)
        self._validate_term(term)
        self._validate_interest_rate(interest_rate)
        
        loc, loc_created = self.create_or_get_loc()
        if not self._can_negotiate(loc):
            last_negotiation = self._get_last_negotiation(loc)
            if last_negotiation.request_creator == self.user:
                raise PermissionDenied(f"You already added a request, please wait for the other party to respond.")
            else:
                raise PermissionDenied(f"You cannot negotiate at this time.")
        
        
        if loc_created and not loc.negotiations.exists():
            LOCNegotiationRequest.objects.create(
                line_of_credit=loc,
                request_creator=self.user,
                term=term,
                interest_rate=interest_rate,
                amount=amount,
                status='OPEN'
            )
        else:
            self._counter_previous_negotiation(loc)
            LOCNegotiationRequest.objects.create(
                line_of_credit=loc,
                request_creator=self.user,
                term=term,
                interest_rate=interest_rate,
                amount=amount,
                status='OPEN'
            )

    def _counter_previous_negotiation(self, loc):
        last_negotiation = self._get_last_negotiation(loc)
        if last_negotiation and last_negotiation.status not in ['ACCEPTED', 'REJECTED', 'CANCELLED']:
            last_negotiation.status = 'COUNTERED'
            last_negotiation.updated_at = timezone.now()
            last_negotiation.save()


    @transaction.atomic
    def accept_negotiation(self, negotiation_id):
        negotiation_to_accept = LOCNegotiationRequest.objects.select_related('line_of_credit').get(pk=negotiation_id)
        
        # Validate the negotiation can be accepted
        if negotiation_to_accept.line_of_credit.loan_request.user != self.user and negotiation_to_accept.request_creator != self.user:
            raise PermissionDenied("Only the loan creator or the negotiator can accept the negotiation.")

        # Counter the previous negotiation if exists
        self._counter_previous_negotiation(negotiation_to_accept.line_of_credit)

        # Create new accepted negotiation request
        accepted_negotiation = LOCNegotiationRequest.objects.create(
            line_of_credit=negotiation_to_accept.line_of_credit,
            request_creator=self.user,
            term=negotiation_to_accept.term,
            interest_rate=negotiation_to_accept.interest_rate,
            amount=negotiation_to_accept.amount,
            status='ACCEPTED'
        )

        # Determine confirmed_by user
        confirmed_by_user = self.user if self.is_lender else ComintUser.objects.get(pk=negotiation_to_accept.line_of_credit.loan_request.user_id)

        # Create LOC confirmation object with confirmed_by as the other party
        LOCConfirmation.objects.create(
            loc_negotiation_request=accepted_negotiation,
            confirmed=False,
            confirmed_by=confirmed_by_user
        )
        
        return accepted_negotiation

    @transaction.atomic
    def confirm_negotiation(self, negotiation_id, confirm=True):
        # Fetch the negotiation and its associated unique confirmation
        negotiation = LOCNegotiationRequest.objects.get(pk=negotiation_id)
        try:
            confirmation = LOCConfirmation.objects.get(loc_negotiation_request=negotiation)
        except LOCConfirmation.DoesNotExist:
            raise PermissionDenied("No confirmation object exists for this negotiation.")
        
        # Check if the negotiation has already been confirmed
        if confirmation.confirmed:
            raise PermissionDenied("This negotiation has already been confirmed.")
        
        # Validate if the negotiation is in an acceptable state and if the user is the correct party
        if negotiation.status != 'ACCEPTED':
            raise PermissionDenied("This negotiation cannot be confirmed because it is not accepted.")
        if self.user != confirmation.confirmed_by:
            raise PermissionDenied("Only the specified party can confirm this negotiation.")
        
        # Update and save the confirmation object
        confirmation.confirmed = confirm
        confirmation.confirmed_at = timezone.now() if confirm else None
        confirmation.save()

        return confirmation

    
    def print_negotiations_for_loc(self, loc):
        negotiations = loc.negotiations.order_by('created_at')
        table_header = "| {:^10} | {:^15} | {:^10} | {:^15} | {:^20} | {:^10} | {:^10} |".format(
            "Negotiation", "Request Creator", "Term (Months)", "Interest Rate (%)", "Amount (USD)", "Created At", "Status"
        )
        table_rows = [table_header]
        for negotiation in negotiations:
            row = "| {:^10} | {:<15} | {:^10} | {:^15.2f} | {:^20} | {:^10} | {:^10} |".format(
                negotiation.id,
                negotiation.request_creator.get_full_name() or negotiation.request_creator.email,
                negotiation.term,
                negotiation.interest_rate,
                "{:.2f}".format(negotiation.amount),
                negotiation.created_at.strftime("%Y-%m-%d %H:%M"),
                negotiation.get_status_display(),
            )
            table_rows.append(row)
        
        return "\n".join(table_rows)

    def get_loc_negotiations_map(self):
        """
        Returns a dictionary mapping each LOC related to the loan request to its negotiation chain.
        """
        loc_negotiations_map = {}
        locs = LineOfCredit.objects.filter(loan_request=self.loan_request)

        # Mapping for status choices
        status_choices = dict(LOCNegotiationRequest.STATUS_CHOICES)

        for loc in locs:
            negotiations = loc.negotiations.order_by('created_at').values(
                'id', 'request_creator__email', 'term', 'interest_rate', 'amount', 'created_at', 'status'
            )
            # Converting datetime and email field for easy access in the template
            formatted_negotiations = [{
                'id': neg['id'],
                'request_creator': neg['request_creator__email'],
                'term': neg['term'],
                'interest_rate': neg['interest_rate'],
                'amount': neg['amount'],
                'created_at': neg['created_at'].strftime("%Y-%m-%d %H:%M"),
                'status': status_choices.get(neg['status'], neg['status'])  # Convert code to human-readable status
            } for neg in negotiations]

            loc_negotiations_map[loc.id] = formatted_negotiations

        return loc_negotiations_map
    
    def get_negotiations_for_loc(self, loc):
        """
        Retrieves and formats negotiations for a given Line of Credit.
        """
        negotiations = loc.negotiations.order_by('created_at')
        # Mapping for status choices
        status_choices = dict(LOCNegotiationRequest.STATUS_CHOICES)

        # Format the negotiations for easy template rendering
        formatted_negotiations = [{
            'id': neg.id,
            'request_creator': neg.request_creator.email,
            'term': neg.term,
            'interest_rate': neg.interest_rate,
            'amount': f"${neg.amount:.2f}",
            'created_at': neg.created_at.strftime("%Y-%m-%d %H:%M"),
            'status': neg.get_status_display()  # Convert code to human-readable status
        } for neg in negotiations]
        return formatted_negotiations
