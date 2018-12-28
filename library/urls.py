from django.urls import path
from django.contrib.auth.decorators import login_required
from .import views

app_name = 'library'

urlpatterns = [
    path('department/', login_required(views.view_courses), name='department'),
    path('department/<int:pk>/', login_required(views.CourseView.as_view()), name='course'),
    path('course/<int:pk>/', login_required(views.CourseDetailView.as_view()), name='detail'),
    path('topic/<int:pk>/', login_required(views.topic_detail), name='topic_detail'),
    path('course/selection/add/', views.add_course_selection, name='add_course_selection'),
    path('course/selection/remove/', views.remove_course_selection, name='remove_course_selection'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
