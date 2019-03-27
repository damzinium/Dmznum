import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseGone, HttpResponseBadRequest, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.models import User
from accounts.utils import get_user
from .models import Topic, Course, Department, Comment, Reply, CourseSelection, SubTopic
from .forms import CommentForm


def department_list(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, 'library/department.html', context)


def list_courses(request):
    required_courses = Course.objects.filter(is_required=True)
    department_list = Department.objects.all()
    course_selections = CourseSelection.objects.filter(user=get_user(request))
    selected_courses = {course_selection.course for course_selection in course_selections}

    paginator = Paginator(department_list, 8)

    page = request.GET.get('page')
    departments = paginator.get_page(page)

    context = {
        'required_courses': required_courses,
        'departments': departments,
        'selected_courses': selected_courses,
    }
    return render(request, 'library/courses.html', context)


@login_required
def department_courses(request, pk):
    department = get_object_or_404(Department,id=pk)
    context = {
        'courses': department.course_set.all()
    }
    return render(request, 'library/course.html', context)



@login_required
def list_topics(request, pk):
    course = get_object_or_404(Course, id=pk)
    try:
        first_topic = Topic.objects.get(course=course, prev=None)
    except Topic.DoesNotExist:
        first_topic = None
    # paginator = Paginator(course_list, 3)

    # page = request.GET.get('page')
    # topics = paginator.get_page(page)

    context = {
        'first_topic': first_topic
    }
    return render(request, 'library/list_topics.html', context)


@login_required
def list_subtopics(request, pk):
    topic = get_object_or_404(Topic, id=pk)
    try:
        first_subtopic = SubTopic.objects.get(topic=topic, prev=None)
    except SubTopic.DoesNotExist:
        first_subtopic = None
    context = {
        'topic': topic,
        'first_subtopic': first_subtopic
    }
    return render(request, 'library/list_subtopics.html', context)


@login_required
def list_subtopic_content(request, pk):
    subtopic = get_object_or_404(SubTopic, id=pk)

    context = {
        'subtopic': subtopic
    }
    return render(request, 'library/list_subtopic_content.html', context)


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


@login_required
def load_comment_app(request, topic_id):
    if request.is_ajax() and request.method == 'GET':
        comments = Comment.objects.filter(topic__id=topic_id)
        context = {
            'topic_id': topic_id,
            'comments': comments,
        }
        return render(request, 'library/comment_app.html', context)
