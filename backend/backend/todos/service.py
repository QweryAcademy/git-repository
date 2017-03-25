from .models import Todo, TodoForm
from ..forms import LoginForm, SignupForm

from django.shortcuts import render
from django.db.models import F, Q


def serialize_model(instance):
    response = {}
    for field in ['id', 'content', 'completed']:
        response[field] = getattr(instance, field)
    return response


def add_logic(data):
    todo_form = TodoForm(data)
    if todo_form.is_valid():
        result = todo_form.save()
        return serialize_model(result), 200
    return todo_form.errors, 400


def delete_logic(id):
    todo = Todo.objects.filter(pk=id).first()
    if todo:
        todo.delete()
        return True
    return False


def update_logic(id):
    todo = Todo.objects.filter(pk=id).first()
    # Todo.objects.filter(pk=pk).update(completed=~F('completed'))
    if todo:
        todo.completed = not todo.completed
        todo.save()
        return serialize_model(todo)
    return False


def bulk_update(data):
    """[
            {'type':'ADD', 'data':{'content': 'hello'}},
            {'type': 'EDIT', 'data': 23},
            {'type': 'DELETE', 'data': 23}        ]"""
    options = {
        'ADD': add_logic,
        'EDIT': update_logic,
        'DELETE': delete_logic,
    }

    for item in data:
        options[item['type']](item['data'])


def authentication_logic(auth_type, request, callback):
    options = {
        'login': LoginForm,
        'signup': SignupForm
    }
    form = options[auth_type]()
    if request.POST:
        form = options[auth_type](request.POST)
        if form.is_valid():
            form.save(request)
            return callback()
    return render(request, "{}.html".format(auth_type), {'form': form})


def get_todos(user):
    return Todo.objects.my_todos(user)
