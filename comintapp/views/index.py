from django.http import HttpResponse

def handleRequest(request):
    return HttpResponse("Hello World")