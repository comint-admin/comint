from django.shortcuts import render

def loanView(request):
    context = {}
    context['username'] = 'Username'
    return render(request, "comintapp/loans.html", context)
