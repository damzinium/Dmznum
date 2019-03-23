from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from library.models import Topic

# Create your views here.
def ShowKitchen(request):
	template_name = 'kitchen/index.html'
	return render(request, template_name)

class PostCreate(CreateView):
	model = Topic
	fields = ['course','title', 'content']
	template_name = 'kitchen/add.html'

# class UgrcPostCreate(PostCreate):
# 	model = Ugrc_Topic
# 	fields = ['ugrc', 'title', 'content']

# Kitchen app here