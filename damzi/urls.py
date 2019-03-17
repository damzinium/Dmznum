from django.urls import path
from . import views


app_name = 'damzi'

urlpatterns = [
	path('', views.index, name='index'),
	path('messages/get/', views.get_messages, name='get_messages'),
]
