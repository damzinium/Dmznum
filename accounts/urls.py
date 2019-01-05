from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', login_required(views.home), name='profile'),
    # path('ots/', login_required(views.OtsView.as_view()), name='ots'),
    path('ots/', login_required(views.ots), name='ots'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),

    # user auth urls
    path('login/', views.ac_login, name='login'),
    path('logout/', views.ac_logout, name='logout'),
    # path('auth/', views.auth_view, name='auth_view'),

    # ugrc
    path('topic/<int:pk>/', (views.UgrcTopicView.as_view()), name='ugrc_detail'),
    path('content/<int:pk>/', (views.UgContent.as_view()), name='content'),

    # password reset
    path('reset_password/', auth_views.PasswordResetView.as_view(success_url='password_reset_done'), name='password_reset'),
    path('reset_password/password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/password_reset_confirm/<slug:uidb64>/<slug:token>',
         auth_views.PasswordResetConfirmView.as_view(success_url='password_reset_complete'),
         name='password_reset_confirm'),
    path('reset_password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('settings/', views.settings, name='settings'),
    path('settings/account/', views.account_settings, name='account_settings'),
    path('settings/security/', views.security_settings, name='security_settings'),
    path('settings/account/profile_picture/update/', views.update_profile_picture, name='update_profile_picture'),
    path('settings/account/names/update/', views.update_names, name='update_names'),
    path('settings/account/phone/update', views.update_phone_number, name='update_phone_number'),
    path('settings/account/email/update/', views.update_email, name='update_email'),
    path('settings/account/institution/update/', views.update_institution, name='update_institution'),
    path('settings/account/department/update/', views.update_department, name='update_department'),
    path('settings/security/password/change/', views.change_password, name='change_password'),
]
