import json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from backend.todos.models import Todo, TodoForm
from django.db.models import F, Q
from backend.todos import service as services
from django.contrib import messages
from django.contrib.auth import (
    login as django_login,
    decorators as django_decorators,
    logout as django_logout)
# Service Layer

# View functions

from functools import wraps
from .forms import LoginForm, SignupForm


def valid_verbs(list_of_verbs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if args[0].method in list_of_verbs:
                return func(*args, **kwargs)
            return JsonResponse({'error': "Method not allowed"}, status=405)
        return wrapper
    return decorator


def login(request):
    form = LoginForm()
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            django_login(request, user)
            return redirect('home_page')
    return render(request, 'login.html', {'form': form})


@django_decorators.login_required
def logout(request):
    django_logout(request)
    messages.info(request, "You are now logged out")
    return redirect('home_page')


def signup(request):
    form = SignupForm()
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            messages.info(request, "You now have an account")
            return redirect('home_page')

    return render(request, 'signup.html', {'form': form})


def hello(request):
    if request.user.is_authenticated():
        user = request.user
        q1 = Q(owner=user)
        q2 = Q(owner=None)
        q3 = q1 | q2
        all_todos = Todo.objects.filter(q3).values(
            "id", 'content', 'completed')
    else:
        all_todos = Todo.objects.filter(owner=None).values(
            'id', 'content', 'completed')
    return render(request, 'index.html', {'all_todos': json.dumps(list(all_todos))})


@valid_verbs(['POST'])
def add_todo(request):
    """"""
    data = json.loads(request.body.decode('utf-8'))
    response, status_code = services.add_logic(data)
    if status_code == 200:
        return JsonResponse(response, status=200)
    return JsonResponse({'errors': response}, status=status_code)


@valid_verbs(['DELETE'])
def delete_todo(request, pk):
    status = services.delete_logic(pk)
    if status:
        return JsonResponse({'status': "Deleted"})
    return JsonResponse({'data': "Todo does not exist"}, status=400)


@valid_verbs(['POST', 'PUT'])
def update_todo(request, pk):
    updated_data = services.update_logic(pk)
    if updated_data:
        return JsonResponse(updated_data)
    return JsonResponse({'data': "Todo does not exist"}, status=400)


@valid_verbs(['POST'])
def bulk_update(request):
    data = json.loads(request.body.decode('utf-8'))
    services.bulk_update(data)
    return JsonResponse({'status': "Batch Succeeded"})
