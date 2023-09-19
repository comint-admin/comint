from django.shortcuts import render

def fundRequests(request):
    context = {}
    context['username'] = 'Username'
    return render(request, "comintapp/fund_requests.html", context)

def payments(request):
    context = {}
    context['username'] = 'Username'
    return render(request, "comintapp/payments.html", context)
