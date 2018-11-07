from django.shortcuts import render_to_response, redirect

# Create your views here.


def index(request):
	if request.user.is_authenticated:
		return redirect('accounts:profile')
	else:
		return redirect('accounts:login')
