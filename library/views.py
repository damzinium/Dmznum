import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseGone, HttpResponseBadRequest, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.models import User
from accounts.utils import get_user
from .models import Topic, Course, Department, Ugrc, Ugrc_Topic, Comment, Reply, CourseSelection
from .forms import CommentForm



# Create your views here.
class DepartmentView(generic.ListView):
    template_name = 'library/department.html'

    def get_queryset(self):
        return Department.objects.all()


def view_courses(request):
    required_courses = Course.objects.filter(is_required=True)
    departments = Department.objects.all()
    course_selections = CourseSelection.objects.filter(user=get_user(request))
    selected_courses = {course_selection.course for course_selection in course_selections}
    context = {
        'required_courses': required_courses,
        'departments': departments,
        'selected_courses': selected_courses,
    }
    return render(request, 'library/department.html', context)


class CourseView(generic.DetailView):
    model = Department
    template_name = 'library/course.html'


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'library/detail.html'


# class TopicDetailView(generic.DetailView):
#     model = Topic
#     template_name = 'library/topic_detail.html'

@login_required
def topic_detail(request, pk):
    topic = get_object_or_404(Topic, id=pk)
    profile_picture = get_object_or_404(User, id=request.user.id).profile.profile_picture
    comment_list = Comment.objects.filter(topic__id=pk, is_approved=False).order_by('-date_uploaded')

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # new_comment = Comment()
            new_comment.commenter = request.user
            new_comment.topic = topic
            # new_comment.comment = comment_form.cleaned_data['comment']
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
            'profile_picture': profile_picture,
        }
        return render(request, 'library/topic_detail.html', context)


def faq(request):
    return render_to_response('library/faq.html')


def about(request):
    return render_to_response('library/about.html')


def contact(request):
    return render_to_response('library/contact.html')


@login_required
def add_course_selection(request):
    if request.is_ajax() and request.method == 'POST':
        already_selected = False
        course_id = request.POST.get('course_id')
        user = get_user(request)
        course = get_object_or_404(Course, id=course_id)
        course_selections = CourseSelection.objects.filter(user=user)
        for course_selection in course_selections:
            if course == course_selection.course:
                already_selected = True
                break
        if not already_selected:
            new_course_selection = CourseSelection()
            new_course_selection.user = user
            new_course_selection.course = course
            new_course_selection.save()
            messages.success(request, 'Successfully added course to your selections.')
            response_obj = {
                'status': 'success',
                'course_id': course_id,
            }
        else:
            messages.error(request, 'You have already selected this course.')
            response_obj = {
                'status': 'error',
            }
    else:
        messages.error(request, 'Could not add course to your selections. Please try again.')
        response_obj = {
            'status': 'error',
        }
    response_json = json.dumps(response_obj)
    return HttpResponse(response_json, content_type='text/json')


@login_required
def remove_course_selection(request):
    if request.is_ajax() and request.method == 'POST':
        user = get_user(request)
        course = get_object_or_404(Course, id=request.POST.get('course_id'))
        course_selection = CourseSelection.objects.get(user=user, course=course)
        course_selection.delete()
        messages.success(request, 'Successfully remove course from your selection.')
        response_obj = {
            'status': 'success',
            'course_id': request.POST.get('course_id'),
        }
    else:
        messages.error(request, 'Could not add course to your selections. Please try again.')
        response_obj = {
            'status': 'error',
        }
    response_json = json.dumps(response_obj)
    return HttpResponse(response_json, content_type='text/json')
