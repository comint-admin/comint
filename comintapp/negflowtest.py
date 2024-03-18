from django.contrib.auth import get_user_model
from comintapp.models import LoanRequest, LineOfCredit, LOCNegotiationRequest
from comintapp.services import LoanService

# Assuming 'your_app_name' is the name of your Django app

# Replace 'UserModel' with your user model name if different
UserModel = get_user_model()

# Create or get users
borrower = UserModel.objects.get_or_create(email='borrower@example.com', defaults={'password':'demo'})[0]
lender = UserModel.objects.get_or_create(email='lender@example.com', defaults={'password':'demo'})[0]

# Create a loan request
loan_request = LoanRequest.objects.create(
    user=borrower,
    term=12,
    interest_rate=5.0,
    amount=4000,
    name='Wedding',
    description='I am getting married'
)

# Create loan service for lender
loan_service_lender = LoanService(loan_request, lender)
loan_service_borrower = LoanService(loan_request, borrower)

# Lender initiates a line of credit
print(f"Lender ({lender.email}) is attempting to initiate a line of credit...")
loc, created = loan_service_lender.create_or_get_loc()

# Lender adds a negotiation request
print("Lender is adding a negotiation request...")
loan_service_lender.add_negotiation_request(amount=19000, term=12, interest_rate=4.5)

# Attempt to add another negotiation request immediately which should fail
print("Lender attempts to add another negotiation request immediately...")
try:
    loan_service_lender.add_negotiation_request(amount=18000, term=12, interest_rate=4.0)
except PermissionDenied as e:
    print(f"Permission denied: {e}")

# Borrower counters the negotiation
print("Borrower is countering the negotiation...")
loan_service_borrower.add_negotiation_request(amount=19500, term=12, interest_rate=4.75)

# Print negotiation chain
print("Negotiation Chain:")
print(loan_service_lender.get_negotiation_chain_as_table(loc))