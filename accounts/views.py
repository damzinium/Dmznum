from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect, get_object_or_404
from django.template.context_processors import csrf
from django.urls import reverse
from django.views import generic
from django.views.generic import View, CreateView

from library.models import Course, CourseSelection, Ugrc, Ugrc_Topic

from . import forms
from .utils import get_user, get_profile
from .models import Profile, User


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
    # redirect user to the dashboard if they are already logged in
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    to_url = request.GET.get('next')

    if request.method == 'POST':
        form = forms.UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            if to_url:
                return redirect(to_url)
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
    return render(request, 'accounts/settings.html')


@login_required
def account_settings(request):
    return render(request, 'accounts/account_settings.html')


@login_required
def update_names(request):
    form_class = forms.NamesUpdateForm
    template_name = 'accounts/update_names.html'
    user = get_user(request)

    if not user:
        return redirect('accounts:logout')

    if request.method == 'POST':
        form = form_class(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your names were successfully updated.')
            return redirect('accounts:account_settings')
        else:
            messages.error(request, 'Some entries were incorrect. Please try again.')
            return render(request, template_name, {'form': form})
    else:
        form = form_class(instance=user)
        return render(request, template_name, {'form': form})


@login_required
def update_email(request):
    form_class = forms.EmailUpdateForm
    template_name = 'accounts/update_email.html'
    user = get_user(request)

    if not user:
        return redirect('accounts:logout')

    if request.method == 'POST':
        form = form_class(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email was successfully updated.')
            return redirect('accounts:account_settings')
        else:
            messages.error(request, 'Some entries were incorrect. Please try again.')
            return render(request, template_name, {'form': form})
    else:
        form = form_class(instance=user)
        return render(request, template_name, {'form': form})


@login_required
def update_institution(request):
    form_class = forms.InstitutionUpdateForm
    template_name = 'accounts/update_institution.html'
    profile = get_profile(request)

    if not profile:
        return redirect('accounts:logout')

    if request.method == 'POST':
        form = form_class(data=request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your institution was successfully updated.')
            return redirect('accounts:account_settings')
        else:
            messages.error(request, 'Some entries were incorrect. Please try again.')
            return render(request, template_name, {'form': form})
    else:
        form = form_class(instance=profile)
        return render(request, template_name, {'form': form})


@login_required
def update_department(request):
    form_class = forms.DepartmentUpdateForm
    template_name = 'accounts/update_department.html'
    profile = get_profile(request)

    if not profile:
        return redirect('accounts:logout')

    if request.method == 'POST':
        form = form_class(data=request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your department was successfully updated.')
            return redirect('accounts:account_settings')
        else:
            messages.error(request, 'Some entries were incorrect. Please try again.')
            return render(request, template_name, {'form': form})
    else:
        form = form_class(instance=profile)
        return render(request, template_name, {'form': form})


@login_required
def update_phone_number(request):
    form_class = forms.PhoneNumberUpdateForm
    template_name = 'accounts/update_phone_number.html'
    profile = get_profile(request)

    if not profile:
        return redirect('accounts:logout')

    if request.method == 'POST':
        form = form_class(data=request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your phone number was successfully updated.')
            return redirect('accounts:account_settings')
        else:
            messages.error(request, 'Some entries were incorrect. Please try again.')
            return render(request, template_name, {'form': form})
    else:
        form = form_class(instance=profile)
        return render(request, template_name, {'form': form})


@login_required
def update_profile_picture(request):
    form_class = forms.ProfilePictureUpdateForm
    template_name = 'accounts/update_profile_picture.html'
    profile = get_profile(request)

    if not profile:
        return redirect('accounts:logout')

    if request.method == 'POST':
        form = form_class(files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile picture was successfully updated.')
            return redirect('accounts:account_settings')
        else:
            messages.error(request, 'Some entries were incorrect. Please try again.')
            return render(request, template_name, {'form': form})
    else:
        form = form_class(instance=profile)
        return render(request, template_name, {'form': form})
