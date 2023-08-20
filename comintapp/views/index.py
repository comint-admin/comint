from django.shortcuts import render

def handleRequest(request):
    context = {}
    context['username'] = 'Username'
    return render(request, "comintapp/index.html", context)