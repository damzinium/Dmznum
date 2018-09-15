from django.shortcuts import render
from django.views.generic.edit import CreateView
from library.models import Topic, Ugrc_Topic

# Create your views here.
class PostCreate(CreateView):
	model = Topic
	fields = ['course_name','title', 'content']
	template_name = 'kitchen/add.html'

class Ugrc_PostCreate(PostCreate):
	model = Ugrc_Topic
	fields = ['ugrc', 'title', 'content']

# Kitchen app here