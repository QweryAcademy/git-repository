from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        instance = super().clean()
        user = User.objects.filter(username=instance['username']).first()
        if user is None:
            raise forms.ValidationError("Please sign up")
        if not user.check_password(instance['password']):
            raise forms.ValidationError("The password is invalid")
        return instance

    def get_user(self):
        user = User.objects.filter(
            username=self.cleaned_data['username']).first()
        logged_in_user = authenticate(**self.cleaned_data)
        if logged_in_user is None:
            raise forms.ValidationError("This credentials is invalid")
        return logged_in_user


class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        instance = super().clean()
        exists = User.objects.filter(username=instance['username']).exists()
        if exists:
            raise forms.ValidationError("This user already exists")
        return instance

    def save(self):
        new_user = User.objects.create(**self.cleaned_data)
        new_user.set_password(self.cleaned_data['password'])
        new_user.save()
        authenticated_user = authenticate(**self.cleaned_data)
        return authenticated_user
