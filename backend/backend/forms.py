from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
# Service Layer


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

    def save(self, request):
        user = User.objects.filter(
            username=self.cleaned_data['username']).first()
        logged_in_user = authenticate(**self.cleaned_data)
        if logged_in_user is None:
            raise forms.ValidationError("This credentials is invalid")
        login(request, logged_in_user)


class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        instance = super().clean()
        exists = User.objects.filter(username=instance['username']).exists()
        if exists:
            raise forms.ValidationError("This user already exists")
        return instance

    def save(self, request):
        new_user = User.objects.create(**self.cleaned_data)
        new_user.set_password(self.cleaned_data['password'])
        new_user.save()
        user = authenticate(**self.cleaned_data)
        login(request, user)
        messages.info(request, "You now have an account")
