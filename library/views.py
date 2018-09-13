from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.models import User
from watson.views import SearchMixin
from .models import Topic, Course, Department, Ugrc, Ugrc_Topic, Comment, Reply
from .forms import CommentForm
from watson.views import SearchMixin


# Create your views here.
class DepartmentView(generic.ListView):
    template_name = 'library/department.html'

    def get_queryset(self):
        return Department.objects.all()


class CourseView(generic.DetailView):
    model = Department
    template_name = 'library/course.html'


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'library/detail.html'

class SearchView(SearchMixin, generic.ListView):

    """View that performs a search and returns the search results."""
    template_name = "library/search.html"


# class TopicDetailView(generic.DetailView):
#     model = Topic
#     template_name = 'library/topic_detail.html'


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, id=pk)
    profile_picture = get_object_or_404(User, id=request.user.id).profile.profile_picture
    comment_list = Comment.objects.filter(topic__id=pk, is_approved=False).order_by('-date_uploaded')

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = Comment()
            new_comment.commenter = request.user
            new_comment.topic = topic
            new_comment.comment = comment_form.cleaned_data['comment']
            new_comment.save()
            # success_msg = 'Thanks for learning smart with damzinium. We appreciate your feedback.'
            return redirect('library:topic_detail', pk=pk)
        else:
            return redirect('library:topic_detail', pk=pk)
    else:
        comment_form = CommentForm
        context = {
            'comment_form': comment_form,
            'comment_list': comment_list,
            'topic': topic,
            # 'success_msg': '',
            'profile_picture': profile_picture,
        }
        return render(request, 'library/topic_detail.html', context)


def faq(request):
    return render_to_response('library/faq.html')


def about(request):
    return render_to_response('library/about.html')


def contact(request):
    return render_to_response('library/contact.html')