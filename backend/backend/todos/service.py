from .models import Todo


def add_logic(data):
    todo_form = TodoForm(data)
    if todo_form.is_valid():
        result = todo_form.save()
        response = {}
        for field in ['id', 'content', 'completed']:
            response[field] = getattr(result, field)
        return response, 200
    return todo_form.errors, 400


def delete_logic(id):
    todo = Todo.objects.filter(pk=pk).first()
    if todo:
        todo.delete()
        return True
    return False


def update_logic(id):
    todo = Todo.objects.filter(pk=pk).first()
    # Todo.objects.filter(pk=pk).update(completed=~F('completed'))
    if todo:
        todo.completed = not todo.completed
        todo.save()
        return True
    return False
