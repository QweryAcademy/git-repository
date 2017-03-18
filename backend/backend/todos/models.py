from django.db import models
from django import forms

# Create your models here.
class Todo(models.Model):
    content = models.TextField()
    completed = models.BooleanField(default=False)

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