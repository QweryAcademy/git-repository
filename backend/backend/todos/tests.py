from test_plus import TestCase
import json
# Create your tests here.
from backend.todos.models import Todo
from django.contrib.auth.models import User


class TodoViewTestCase(TestCase):
    def test_can_successfully_add_a_todo(self):
        self.assertEqual(Todo.objects.count(), 0)
        url = self.reverse('add_todo')
        response = self.client.post(url, data=json.dumps({
            'content': "This is a new Todo"
        }), content_type='application/json')
        self.response_200(response)
        # import ipdb; ipdb.set_trace()
        result = response.json()
        self.assertEqual(result['content'], "This is a new Todo")
        self.assertIn('id', result.keys())
        self.assertFalse(result['completed'])
        self.assertEqual(Todo.objects.count(), 1)

    def test_can_add_new_todo_that_is_completed(self):
        url = self.reverse('add_todo')
        response = self.client.post(url, data=json.dumps({
            'content': "This is a new Todo",
            'completed': True,
        }), format='json', content_type='application/json')
        result = response.json()
        self.assertTrue(result['completed'])

    def test_can_edit_an_existing_todo(self):
        sample_todo = Todo.objects.create(content='Hello world')
        self.assertFalse(sample_todo.completed)
        url = self.reverse('update_todo', sample_todo.id)
        response = self.client.put(
            url, data='', content_type='application/json')

        result = response.json()
        self.assertEqual(result['content'], 'Hello world')
        self.assertEqual(result['id'], sample_todo.id)
        new_sample_todo = Todo.objects.get(pk=sample_todo.pk)
        self.assertTrue(new_sample_todo.completed)

    def test_can_delete_an_existing_todo(self):
        sample_todo = Todo.objects.create(content='Hello world')
        url = self.reverse('delete_todo', sample_todo.id)
        response = self.client.delete(
            url, data='', content_type='application/json')
        self.assertEqual(Todo.objects.count(), 0)
        self.response_200(response)

    def test_throws_400_error_when_todo_id_doesnt_exists(self):
        url = self.reverse('delete_todo', 3)
        response = self.client.delete(
            url, data='', content_type='application/json')
        self.response_400(response)

    def test_throws_400_error_when_todo_id_doesnt_exists_when_editing(self):
        url = self.reverse('update_todo', 3)
        response = self.client.put(
            url, data='', content_type='application/json')
        self.response_400(response)

    def test_bulk_update_implementation_works(self):
        sample_todo = Todo.objects.create(content='Hello world')
        sample_todo2 = Todo.objects.create(content='Hello world23')
        self.assertEqual(Todo.objects.count(), 2)
        url = self.reverse('bulk_update')
        response = self.client.post(url, json.dumps([
            {'type': 'ADD', 'data': {'content': "Hello World to me"}},
            {'type': 'ADD', 'data': {'content': "Hello World to me and you"}},
            {'type': 'EDIT', 'data': sample_todo.id},
            {'type': 'DELETE', 'data': sample_todo2.pk}
        ]), content_type="application/json")
        self.response_200(response)
        self.assertEqual(Todo.objects.count(), 3)
        self.assertIsNone(Todo.objects.filter(pk=sample_todo2.pk).first())

    def test_only_post_method_allowed_for_adding(self):
        url = self.reverse('add_todo')
        response = self.client.put(url, data=json.dumps({
            'content': "This is a new Todo",
            'completed': True,
        }), format='json', content_type='application/json')
        self.response_405(response)
        response = self.client.get(url, data={
            'content': "This is a new Todo",
            'completed': True,
        }, format='json', content_type='application/json')
        self.response_405(response)
        response = self.client.delete(url, data=json.dumps({
            'content': "This is a new Todo",
            'completed': True,
        }), format='json', content_type='application/json')
        self.response_405(response)

    def test_only_put_and_post_method_is_supported_for_editing(self):
        sample_todo = Todo.objects.create(content='Hello world')
        url = self.reverse('update_todo', sample_todo.id)
        response = self.client.get(
            url, data='', content_type='application/json')
        self.response_405(response)
        response = self.client.delete(
            url, data='', content_type='application/json')
        self.response_405(response)
        response = self.client.post(
            url, data='', content_type='application/json')
        self.response_200(response)

    def test_delete_method_only_uses_delete_verb(self):
        url = self.reverse('delete_todo', 3)
        response = self.client.get(
            url, data='', content_type='application/json')
        self.response_405(response)
        response = self.client.post(
            url, data='', content_type='application/json')
        self.response_405(response)

    def test_bulk_update_only_uses_post_verb(self):
        sample_todo = Todo.objects.create(content='Hello world')
        sample_todo2 = Todo.objects.create(content='Hello world23')

        url = self.reverse('bulk_update')
        response = self.client.put(url, json.dumps([
            {'type': 'ADD', 'data': {'content': "Hello World to me"}},
            {'type': 'ADD', 'data': {'content': "Hello World to me and you"}},
            {'type': 'EDIT', 'data': sample_todo.id},
            {'type': 'DELETE', 'data': sample_todo2.pk}
        ]), content_type="application/json")
        self.response_405(response)
        response = self.client.delete(url, json.dumps([
            {'type': 'ADD', 'data': {'content': "Hello World to me"}},
            {'type': 'ADD', 'data': {'content': "Hello World to me and you"}},
            {'type': 'EDIT', 'data': sample_todo.id},
            {'type': 'DELETE', 'data': sample_todo2.pk}
        ]), content_type="application/json")
        self.response_405(response)


class IndexPageTestCase(TestCase):
    def setUp(self):
        Todo.objects.create(content="1")
        Todo.objects.create(content="2")
        self.user = User.objects.create(
            username="biola", email='b@example.com')
        Todo.objects.create(content="3", owner=self.user)

    def test_when_not_logged_in_displays_two_todos(self):
        url = self.reverse('home_page')
        response = self.client.get(url)
        context = response.context
        todos_with_no_user = Todo.objects.filter(
            owner=None).values('content', 'id', 'completed')
        self.assertIn('all_todos', context)
        all_todos = json.loads(context['all_todos'])
        self.assertEqual(len(all_todos), todos_with_no_user.count())
        self.assertEqual(all_todos[0], todos_with_no_user[0])
        # no_user =
        # self.assertEqual(

    def test_when_user_is_authenticated(self):
        self.user.set_password('password')
        self.user.save()
        url = self.reverse('login')
        response = self.client.post(url,
                                    {"username": self.user.username,
                                     "password": 'password'})
        new_url = response.url
        response = self.client.get(new_url)
        context = response.context
        todos_with_no_user = Todo.objects.filter(
            owner=None).values('content', 'id', 'completed')
        self.assertIn('all_todos', context)
        all_todos = json.loads(context['all_todos'])
        self.assertEqual(len(all_todos), 3)

    def test_when_user_signs_up_with_existing_user(self):
        url = self.reverse('register')
        response = self.client.post(url, {'username': self.user.username,
                                          'password': 'password'})
        self.response_200(response)
        form = response.context['form']
        self.assertEqual(['This user already exists'], form.errors['__all__'])
