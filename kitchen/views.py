from django.shortcuts import render
from django.views.generic.edit import CreateView
from library.models import Course, Topic

# Create your views here.
class PostCreate(CreateView):
	model = Topic
	fields = ['course_name','title', 'content']
	template_name = 'kitchen/add.html'

# Kitchen app here