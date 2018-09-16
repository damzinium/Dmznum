from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect, get_object_or_404
from django.template.context_processors import csrf
from django.urls import reverse
from django.views import generic
from django.views.generic import View, CreateView

from library.models import Ugrc, Ugrc_Topic

from .forms import UserRegistrationForm, ProfileForm, UserLoginForm
from .models import Profile, User


# sign up here
class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    # display blank form
    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    # process and register users
    def post(self, request):
        form = self.form_class(request.POST)
        context = {'form': form}

        if form.is_valid():
            user = form.save(commit=False)

            # clean data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
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


# def ac_login(request):
#     c = {}
#     c.update(csrf(request))
#     return render_to_response('accounts/login.html', c)


# def auth_view(request):
#     username = request.POST.get('username', '')
#     password = request.POST.get('password', '')
#     user = auth.authenticate(username=username, password=password)

#     if user is not None:
#         auth.login(request, user)
#         # return HttpResponseRedirect('/library/department')
#         return HttpResponseRedirect('/accounts/')
#     else:
#         return HttpResponseRedirect('/accounts/login')


def ac_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            return redirect('accounts:profile')
        else:
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = UserLoginForm
        return render(request, 'accounts/login.html', {'form': form})


def ac_logout(request):
    logout(request)


# class OtsView(CreateView):
#     model = Profile
#     fields = ['school_name', 'department_name', 'phone_number', 'date_of_birth']
#     template_name = 'accounts/ots.html'
#     success_url = '/accounts/'

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(OtsView, self).form_valid(form)

#     # def get_absolute_url(self):
#     #     return reverse('accounts:profile')


def ots(request):
    # POST request
    if request.method == 'POST':
        # load the form with the posted data
        form = ProfileForm(data=request.POST, files=request.FILES)
        # check for validity
        if form.is_valid():
            user = get_object_or_404(User, id=request.user.id)
            user.profile.profile_picture = form.cleaned_data['profile_picture']
            user.profile.institution = form.cleaned_data['institution']
            user.profile.department_name = form.cleaned_data['department_name']
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
        form = ProfileForm
        return render(request, 'accounts/ots.html', {'form': form})


# ugrc
class Dashboard(generic.ListView):
    template_name = 'accounts/profile.html'

    def get_queryset(self):
        return Ugrc.objects.all()


@login_required
def name_profile(request):
    return render_to_response('accounts/name.html', {'full_name': request.user.username})


class UgrcTopicView(generic.DetailView):
    model = Ugrc
    template_name = 'accounts/ugrc_topics.html'


class UgContent(generic.DetailView):
    model = Ugrc_Topic
    template_name = 'accounts/ugrc_content.html'
