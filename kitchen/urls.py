from django.urls import path
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from . import views

app_name = 'kitchen'

urlpatterns = [
    path('', views.index, name='index'),
    path('departments/', views.list_departments, name='list_departments'),
    path('department/<uuid:department_id>/courses/', views.list_main_courses, name='list_main_courses'),
    path('department/course/<uuid:course_id>/topics/', views.list_topics, name='list_topics'),
    path('department/course/topic/<uuid:topic_id>/subtopics/', views.list_subtopics, name='list_subtopics'),
    path('department/course/topic/subtopic/<uuid:subtopic_id>/edit/content/', views.edit_subtopic_content, name='edit_subtopic_content'),
    path('department/course/topic/subtopic/<uuid:subtopic_id>/edit/info/', views.edit_subtopic_info, name='edit_subtopic_info'),

    path('department/<uuid:department_id>/courses/add/', views.add_main_course, name='add_main_course'),
    path('department/course/<uuid:course_id>/topics/add/', views.add_topic, name='add_topic'),
    path('department/course/topic/<uuid:topic_id>/subtopics/add/', views.add_subtopic, name='add_subtopic'),

    path('required/courses/add/', views.add_required_course, name='add_required_course'),
    
    path('required/courses/', views.list_required_courses, name='list_required_courses'),

]