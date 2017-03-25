import json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from backend.todos.models import Todo, TodoForm
from backend.todos import service as services
from django.contrib import messages
from django.contrib.auth import (
    decorators as django_decorators,
    logout as django_logout)
# Service Layer

# View functions

from functools import wraps


def valid_verbs(list_of_verbs):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.method in list_of_verbs:
                return func(request, *args, **kwargs)
            return JsonResponse({'error': "Method not allowed"}, status=405)
        return wrapper
    return decorator


def login(request):
    return services.authentication_logic('login', request, lambda: redirect('home_page'))


@django_decorators.login_required
def logout(request):
    django_logout(request)
    messages.info(request, "You are now logged out")
    return redirect('home_page')


def signup(request):
    return services.authentication_logic('signup', request, lambda: redirect('home_page'))


def hello(request):
    all_todos = services.get_todos(request.user)
    return render(request, 'index.html', {'all_todos': json.dumps(list(all_todos))})


@valid_verbs(['POST'])
def add_todo(request):
    """"""
    data = json.loads(request.body.decode('utf-8'))
    response, status_code = services.add_logic(data)
    if status_code == 200:
        return JsonResponse(response, status=200)
    return JsonResponse({'errors': response}, status=status_code)

# valid_verbs(['POST'])(add_todo)


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
