from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import Profile, School
from .helpers import generate_years_for_bday, is_phone_number

class UserForm(forms.ModelForm):
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

def save(self, commit=True):
    user = super(UserForm, self).save(commit=False)
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name']
    user.email = self.cleaned_data['email']

    user.set_password(self.cleaned_data['password'])

    if commit:
        user.save()

    return user


class ProfileForm(forms.ModelForm):
    # school_name = forms.ModelChoiceField(queryset=School.objects.all(), widget=forms.Select(attrs={
    #     'class': 'form-control-select',
    # }))

    # phone_number = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control-text',
    # }), help_text='Enter your phone number. eg: 0272727388')

    # date_of_birth = forms.DateField(widget=forms.SelectDateWidget(attrs={
    #     'class': 'form-control-select',
    # },
    #     years=generate_years_for_bday(),
    # ))

    def clean_phone_number(self):
        """
        custom validation for the phone number
        :return:
        """
        phone_number = self.cleaned_data['phone_number']
        if not is_phone_number(phone_number):
            raise ValidationError('Please enter a valid number. eg: 0242425222.')
        return phone_number

    class Meta:
        model = Profile
        fields = [
            'school_name',
            'department_name',
            'phone_number',
            'date_of_birth'
        ]

        

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)

        if commit:
            user.save()

        return user