from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from library.models import Course, Department, SubTopic, Topic

from .forms import AddCourseForm, AddTopicForm, AddSubTopicForm, EditSubTopicContentForm, EditSubTopicInfoForm


@user_passes_test(lambda u: u.is_staff)
@login_required
def index(request):
    template_name = 'kitchen/index.html'
    return render(request, template_name)


@user_passes_test(lambda u: u.is_staff)
@login_required
def list_departments(request):
    template_name = 'kitchen/list_departments.html'
    departments = Department.objects.all()
    context = {
        'departments': departments,
    }
    return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def list_required_courses(request):
    template_name = 'kitchen/list_required_courses.html'
    courses = Course.objects.filter(is_required=True)
    context = {
        'courses': courses,
    }
    return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def list_main_courses(request, department_id):
    template_name = 'kitchen/list_main_courses.html'
    department = get_object_or_404(Department, id=department_id)
    courses = Course.objects.filter(department=department)
    context = {
        'department': department,
        'courses': courses,
    }
    return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def list_topics(request, course_id):
    template_name = 'kitchen/list_topics.html'
    course = get_object_or_404(Course, id=course_id)
    topics = Topic.get_topics_as_list(course)
    context = {
        'course': course,
        'topics': topics,
    }
    return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def list_subtopics(request, topic_id):
    template_name = 'kitchen/list_subtopics.html'
    topic = get_object_or_404(Topic, id=topic_id)
    subtopics = SubTopic.get_subtopics_as_list(topic)
    context = {
        'topic': topic,
        'subtopics': subtopics,
    }
    return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def edit_subtopic_content(request, subtopic_id):
    template_name = 'kitchen/edit_subtopic_content.html'
    form = EditSubTopicContentForm
    subtopic = get_object_or_404(SubTopic, id=subtopic_id)
    if request.method == 'POST':
        form = form(data=request.POST, instance=subtopic)
        if form.is_valid():
            form.save()
            return redirect('kitchen:edit_subtopic_content', subtopic_id=subtopic.id)
        else:
            context = {
                'subtopic': subtopic,
                'form': form,
            }
            return render(request, template_name, context)
    else:
        form = form(instance=subtopic)
        context = {
            'subtopic': subtopic,
            'form': form,
        }
        return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def edit_subtopic_info(request, subtopic_id):
    template_name = 'kitchen/edit_subtopic_info.html'
    form = EditSubTopicInfoForm
    subtopic = get_object_or_404(SubTopic, id=subtopic_id)
    if request.method == 'POST':
        form = form(data=request.POST, instance=subtopic)
        if form.is_valid():
            form.save()
            return redirect('kitchen:edit_subtopic_content', subtopic_id=subtopic.id)
    else:
        form = form(instance=subtopic)
        context = {
            'form': form,
        }
        return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def add_main_course(request, department_id):
    template_name = 'kitchen/add_main_course.html'
    form = AddCourseForm
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        form = form(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.department = department
            new_course.save()
            return redirect('kitchen:list_main_courses', department_id=department_id)
    else:
        context = {
            'form': form
        }
        return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def add_required_course(request):
    template_name = 'kitchen/add_required_course.html'
    form = AddCourseForm
    if request.method == 'POST':
        form = form(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.is_required = True
            new_course.save()
            return redirect('kitchen:list_required_courses')
    else:
        context = {
            'form': form,
        }
        return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def add_topic(request, course_id):
    template_name = 'kitchen/add_topic.html'
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = AddTopicForm(data=request.POST, initial={'course': course})
        if form.is_valid():
            form.save()
            return redirect('kitchen:list_topics', course_id=course_id)
        else:
            return render(request, template_name, {'form': form})
    else:
        context = {
            'form': AddTopicForm(initial={'course': course})
        }
        return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def add_subtopic(request, topic_id):
    template_name = 'kitchen/add_subtopic.html'
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = AddSubTopicForm(data=request.POST, initial={'topic': topic})
        if form.is_valid():
            form.save()
            return redirect('kitchen:list_subtopics', topic_id=topic_id)
        else:
            return render(request, template_name, {'form': form})
    else:
        context = {
            'form': AddSubTopicForm(initial={'topic': topic}),
        }
        return render(request, template_name, context)
