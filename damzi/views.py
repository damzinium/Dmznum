from django.shortcuts import render_to_response
from django.contrib import auth

# Create your views here.
def index(request):
    auth.logout(request)
    return render_to_response('accounts/ots.html')