from .models import Todo, TodoForm

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



options = {
    'ADD': add_logic,
    'EDIT': update_logic,
    'DELETE': delete_logic,
}
"""[
            {'type':'ADD', 'data':{'content': 'hello'}},
            {'type': 'EDIT', 'data': 23},
            {'type': 'DELETE', 'data': 23}        ]"""