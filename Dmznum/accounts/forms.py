from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .helpers import generate_years_for_bday, is_phone_number
from .models import Profile, User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password'
        ]

    def clean_first_name(self):
        return self.cleaned_data['first_name'].upper()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].upper()


def save(self, commit=True):
    user = super(UserRegistrationForm, self).save(commit=False)
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name']
    user.email = self.cleaned_data['email']

    user.set_password(self.cleaned_data['password'])

    if commit:
        user.save()

    return user


class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control-text',
    }), help_text='Enter your phone number. eg: 0272727388')

    # date_of_birth = forms.DateField(widget=forms.SelectDateWidget(
    #     years=generate_years_for_bday(),
    # ))

    def clean_phone_number(self):
        """
        custom validation for the phone number
        :return: the phone number if valid
        """
        phone_number = self.cleaned_data['phone_number']
        if not is_phone_number(phone_number):
            raise ValidationError('Please enter a valid number. eg: 0242425222.')
        return phone_number

    class Meta:
        model = Profile
        fields = [
            'profile_picture',
            'institution',
            'department_name',
            'phone_number',
            'level'
        ]       

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)

        if commit:
            user.save()

        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255, label="Email or Username")
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()

        _ = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=_, password=password)
        if user is None:
            try:
                username = User.objects.get(email=_).username
                user = authenticate(username=username, password=password)
            except User.DoesNotExist:
                user = None
                raise ValidationError('Incorrect username or email or password.')
        if user is not None:
            self.user = user
            return self
