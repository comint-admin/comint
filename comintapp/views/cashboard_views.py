from django.views.generic import TemplateView

class CashboardView(TemplateView):
    template_name = 'comintapp/cashboard.html'

class LenderView(TemplateView):
    template_name = 'comintapp/lender_dashboard.html'

class BorrowerView(TemplateView):
    template_name = 'comintapp/borrower_dashboard.html'
