import json
from django.shortcuts import render
from django.http.response import JsonResponse
from backend.todos.models import Todo, TodoForm
from django.db.models import F
from backend.todos import service as services
# Service Layer

# View functions

from functools import wraps


def valid_verbs(list_of_verbs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if args[0].method in list_of_verbs:
                return func(*args, **kwargs)
            return JsonResponse({'error': "Method not allowed"}, status=405)
        return wrapper
    return decorator


def hello(request):
    all_todos = Todo.objects.values('id', 'content', 'completed')
    return render(request, 'index.html', {'all_todos': json.dumps(list(all_todos))})


@valid_verbs(['POST'])
def add_todo(request):
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
    for item in data:
#        services.implement(item)
        services.options[item['type']](item['data'])
    return JsonResponse({'status': "Batch Succeeded"})
