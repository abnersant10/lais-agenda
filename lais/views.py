from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def login(request):
    if request.method == 'POST':
        return HttpResponse("aeeer")
    return render(request, "login.html")
