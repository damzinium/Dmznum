from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render


def index(request):
	if request.user.is_authenticated:
		return redirect('accounts:profile')
	else:
		return redirect('accounts:login')


def get_messages(request):
	if request.is_ajax():
		return render(request, 'damzi/messages.html')
	else:
		return HttpResponseBadRequest('request was badly formed')
