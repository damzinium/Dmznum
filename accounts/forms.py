from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from library.models import Department
from .utils import is_phone_number
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


class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control-text',
    }), help_text='Enter your phone number. eg: 0272727388')

    # date_of_birth = forms.DateField(widget=forms.SelectDateWidget(
    #     years=generate_years_for_bday(),
    # ))

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not is_phone_number(phone_number):
            raise ValidationError('Please enter a valid number. eg: 0242425222.')
        return phone_number

    class Meta:
        model = Profile
        fields = [
            'profile_picture',
            'institution',
            # 'department',
            'level',
            'phone_number',
            # 'date_of_birth'
        ]

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)

        if commit:
            user.save()

        return user


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={
            'placeholder': 'Email or Username',
            'class': 'form-control',
            'autocomplete': 'off',
            'onkeyup': 'loginBtnStateHandler()',
            'onchange': 'loginBtnStateHandler()'
        })
    )
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'onkeyup': 'loginBtnStateHandler()',
            'onchange': 'loginBtnStateHandler()'
        }
    ))

    def clean(self):
        cleaned_data = super().clean()

        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        user = authenticate(username=username_or_email, password=password)
        if user is None:
            try:
                username = User.objects.get(email=username_or_email).username
                user = authenticate(username=username, password=password)
            except User.DoesNotExist:
                user = None
                raise ValidationError('Incorrect username or email or password.')
        if user is not None:
            self.user = user
            return self


class NamesUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            })
        }


class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            })
        }


class InstitutionUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('institution', )
        widgets = {
            'institution': forms.Select(attrs={
                'class': 'form-control',
            })
        }


class DepartmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('department', )
        widgets = {
            'department': forms.Select(attrs={
                'class': 'form-control',
            })
        }


class LevelUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('level', )


class PhoneNumberUpdateForm(forms.ModelForm):
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not is_phone_number(phone_number):
            raise ValidationError('Please enter a valid number. eg: 0242425222.')
        return phone_number

    class Meta:
        model = Profile
        fields = ('phone_number', )
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            })
        }


class ProfilePictureUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture', )
        widget = {
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            })
        }
