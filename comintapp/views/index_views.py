from django.shortcuts import render

def handleRequest(request):
    context = {}
    if request.user.is_authenticated:
        # Assuming 'first_name' is a field on your custom user model
        context['username'] = request.user.first_name if request.user.first_name else request.user.email
    else:
        context['username'] = 'User'
    return render(request, "comintapp/index.html", context)
