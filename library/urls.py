from django.urls import path
from django.contrib.auth.decorators import login_required
from .import views

app_name = 'library'

urlpatterns = [
    path('courses/', views.list_courses, name='list_courses'),
    path('course/<uuid:pk>/topics/', login_required(views.list_topics), name='list_topics'),
    path('course/topic/<uuid:pk>/sub-topics/', views.list_subtopics, name='list_subtopics'),
    path('course/topic/sub-topic/<uuid:pk>/content/', views.list_subtopic_content, name='list_subtopic_content'),
    path('topic/<uuid:pk>/', login_required(views.topic_detail), name='topic_detail'),
    path('course/selection/add/', views.add_course_selection, name='add_course_selection'),
    path('course/selection/remove/', views.remove_course_selection, name='remove_course_selection'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # special urlpatterns
    path('comment_app/load/<topic_id>/', views.load_comment_app, name='load_comment_app'),
]
