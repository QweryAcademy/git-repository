from django.db import models
from django import forms
# from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Todo(models.Model):
    content = models.TextField()
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='all_todos')

    def __repr__(self):
        return "<Todo: {}>".format(self.content)


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['content','completed']

# class TodoForm2(forms.Form):
#     content = forms.CharField()

#     def save(self, commit=False):
#         if self.is_valid():
#             new_model = Todo(**self.cleaned_data)
#             if commit:
#                 return new_model.save()
#             return new_model
#         else:
#             raise forms.ValidationError("ejwojeow")