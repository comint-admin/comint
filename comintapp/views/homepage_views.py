from django.shortcuts import render

def handleRequest(request):
    context = {}
    return render(request, "comintapp/homepage.html", context)