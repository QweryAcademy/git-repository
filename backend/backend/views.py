import json
from django.shortcuts import render
from django.http.response import JsonResponse
from backend.todos.models import Todo, TodoForm
from django.db.models import F
from backend.todos import service as services
# Service Layer

# View functions


def hello(request):
    all_todos = Todo.objects.values('id', 'content', 'completed')
    return render(request, 'index.html', {'all_todos': json.dumps(list(all_todos))})


def add_todo(request):
    data = json.loads(request.body.decode('utf-8'))
    response, status_code = services.add_logic(data)
    if status_code == 200:
        return JsonResponse(response, status=200)
    return JsonResponse({'errors': response}, status=status_code)


def delete_todo(request, pk):
    status = services.delete_logic(pk)
    if status:
        return JsonResponse({'status': "Deleted"})
    return JsonResponse({'data': "Todo does not exist"}, status=400)


def update_todo(request, pk):
    status = services.update_logic(pk)
    if status:
        return JsonResponse({'status': "Updated"})
    return JsonResponse({'data': "Todo does not exist"}, status=400)


def bulk_update(request):
    options = {
        'ADD': services.add_logic,
        'EDIT': services.update_logic,
        'DELETE': services.delete_logic,
    }
    """[
        {'type':'ADD', 'data':{'content': 'hello'}},
        {'type': 'EDIT', 'data': 23},
        {'type': 'DELETE', 'data': 23}
    ]"""
    data = json.loads(request.body.decode('utf-8'))
    for item in data:
        options[item['type']](item['data'])
    return JsonResponse({'status': "Batch Succedded"})
