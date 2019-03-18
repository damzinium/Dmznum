from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views import generic
from django.views.generic import View

from library.models import CourseSelection, Ugrc, Ugrc_Topic
from . import forms
from .models import User


# sign up here
class UserRegistrationView(View):
    form_class = forms.UserRegistrationForm
    template_name = 'accounts/register.html'

    # display blank form
    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    # process and register users
    def post(self, request):
        form = self.form_class(request.POST)
        context = {
            'form': form,
        }

        if form.is_valid():
            user = form.save(commit=False)

            # clean data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # login after sign up
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    # messages.success('Successfully logged in.')
                    return redirect('accounts:ots')

        return render(request, self.template_name, context)


def ac_login(request):
    # redirect user to the homepage if they are already logged in
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    # get the next page's URL from the current URL
    to_url = request.GET.get('next')

    # if the request is a POST request
    if request.method == 'POST':
        form = forms.UserLoginForm(data=request.POST)
        if form.is_valid():
            # get the value of the `username_or_email` field
            username_or_email = form.cleaned_data.get('username_or_email')

            # get the value of the `password` field
            password = form.cleaned_data.get('password')

            # authenticate the user with `username_or_email` or `password`
            # if the user entered a correct username, the authentication is successful
            # else authentication fails
            user = authenticate(username=username_or_email, password=password)

            # if authentication fails, then its likely the user entered an email address
            # so try to get the username corresponding to the email if it is correct
            # and try authentication with that username and the password
            if user is None:
                try:
                    username = User.objects.get(email=username_or_email).username
                    user = authenticate(username=username, password=password)
                except User.DoesNotExist:
                    user = None
            # if authentication is successful, log the user in
            # otherwise go back to the login page
            if user is not None:
                login(request, user)
            else:
                return render(request, 'accounts/login.html', {'form': form})

            # if the user is a staff, sessions expire when he/she close his/her browser
            if user.is_staff:
                request.session.set_expiry(0)

            # if there's a URL to the next page, then go there
            if to_url:
                return redirect(to_url)
            
            # otherwise go to the homepage
            return redirect('accounts:profile')
        else:
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = forms.UserLoginForm
        return render(request, 'accounts/login.html', {'form': form})


def ac_logout(request):
    logout(request)
    return redirect('accounts:login')


def ots(request):
    # POST request
    if request.method == 'POST':
        # load the form with the posted data
        form = forms.ProfileForm(data=request.POST, files=request.FILES)
        # check for validity
        if form.is_valid():
            user = get_object_or_404(User, id=request.user.id)
            user.profile.profile_picture = form.cleaned_data['profile_picture']
            user.profile.institution = form.cleaned_data['institution']
            # user.profile.department = form.cleaned_data['department']
            user.profile.level = form.cleaned_data['level']
            user.profile.phone_number = form.cleaned_data['phone_number']
            # user.profile.date_of_birth = form.cleaned_data['date_of_birth']
            user.save()
            return redirect('accounts:profile')
        else:
            # return the form rendered with errors
            return render(request, 'accounts/ots.html', {'form': form})
    # other requests
    else:
        form = forms.ProfileForm
        return render(request, 'accounts/ots.html', {'form': form})



# ugrc
# class Dashboard(generic.ListView):
#     template_name = 'accounts/profile.html'
#
#     def get_queryset(self):
#         return Ugrc.objects.all()

@login_required
def home(request):
    course_selections = CourseSelection.objects.filter(user=get_user(request))
    selected_courses = {course_selection.course for course_selection in course_selections}
    return render(request, 'accounts/profile.html', {'selected_courses': selected_courses, })


@login_required
def name_profile(request):
    return render_to_response('accounts/name.html', {'full_name': request.user.username})


class UgrcTopicView(generic.DetailView):
    model = Ugrc
    template_name = 'accounts/ugrc_topics.html'


class UgContent(generic.DetailView):
    model = Ugrc_Topic
    template_name = 'accounts/ugrc_content.html'


def error(request):
    return render_to_response('accounts/error_page.html')


@login_required
def settings(request):
    user = get_user(request)
    return render(request, 'accounts/settings.html')


def account_settings(request):
    if request.is_ajax():
        user = get_user(request)
        if user.is_authenticated:
            context = {
                'account_settings_form': forms.AccountSettingsForm(instance=user),
                'profile_settings_form': forms.ProfileSettingsForm(instance=user.profile),
            }
            return render(request, 'accounts/account_settings.html', context)
        else:
            return HttpResponseBadRequest('Bad Request')
    else:
        return HttpResponseBadRequest('Bad Request')


def security_settings(request):
    if request.is_ajax():
        user = get_user(request)
        if user.is_authenticated:
            return render(request, 'accounts/security_settings.html')
        else:
            return HttpResponseBadRequest('Bad Request')
    else:
        return HttpResponseBadRequest('Bad Request')
