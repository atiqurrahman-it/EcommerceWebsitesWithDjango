from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


class SingUpCreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label="",
                             widget=forms.TextInput(attrs={'placeholder': 'Email ', 'type': 'email', }))

    password1 = forms.CharField(required=True,
                                label='',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(required=True,
                                label='',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
