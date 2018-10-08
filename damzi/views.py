from django.shortcuts import render_to_response, redirect
from django.contrib import auth

# Create your views here.
def index(request):
    auth.logout(request)
    return redirect('accounts:login')
