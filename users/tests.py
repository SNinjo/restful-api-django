from typing import Any, List
from django.http import HttpResponse
from django.test import SimpleTestCase
from users.models import User

class TestUsersView(SimpleTestCase):
    def setUp(self):
        User.drop_collection()

    @classmethod
    def tearDownClass(cls):
        User.drop_collection()

    fake_user_id = '012345678901234567890123'

    def has_error_in_response(self, response: HttpResponse) -> bool:
        return 'error' in response.json()

    def is_user_valid(self, data: Any, name: str, age: int) -> bool:
        if 'id' not in data:
            return False
        if 'created_at' not in data:
            return False
        if 'updated_at' not in data:
            return False
        if 'name' not in data or data['name'] != name:
            return False
        if 'age' not in data or data['age'] != age:
            return False
        return True
    
    def create_users_to_database(self, users: List[User]) -> None:
        for user in users:
            user.save()
    
    def is_all_users_in_database(self, users: List[User]) -> bool:
        userObjects = User.objects().all() # type: ignore
        if len(users) != len(userObjects):
            return False
        for index in range(len(users)):
            user = users[index]
            if not self.is_user_valid(userObjects[index], user.name, user.age): # type: ignore
                return False
        return True
    
class TestGetMethod(TestUsersView):

    def test_normal(self):
        users = [
            User(name='jo', age=20),
            User(name='alan', age=21),
        ]
        self.create_users_to_database(users)

        response = self.client.get(f'/users/?id={users[0].id}') # type: ignore
        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertTrue(self.is_user_valid(response.json(), 'jo', 20))

    def test_safe(self):
        users = [
            User(name='jo', age=20),
            User(name='alan', age=21),
        ]
        self.create_users_to_database(users)

        self.client.get(f'/users/?id={users[0].id}') # type: ignore
        self.assertTrue(self.is_all_users_in_database(users))
        
        self.client.get(f'/users/?id={users[0].id}') # type: ignore
        self.assertTrue(self.is_all_users_in_database(users))

    def test_fake_user_id(self):
        user = User(name='jo', age=20)
        user.save()

        response = self.client.get(f'/users/?id={self.fake_user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)
        self.assertTrue(self.is_all_users_in_database([user]))

class TestPostMethod(TestUsersView):

    def test_normal(self):
        response = self.client.post('/users/', {
            'name': 'jo',
            'age': 20,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.is_user_valid(response.json(), 'jo', 20))
        self.assertTrue(self.is_all_users_in_database([
            User(name='jo', age=20),
        ]))
        
        response = self.client.post('/users/', {
            '_id': self.fake_user_id,
            'id': self.fake_user_id,
            'fake': 'fake',
            'name': 'alan',
            'age': 21,
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertNotEqual(data['id'], self.fake_user_id)
        self.assertTrue(self.is_user_valid(data, 'alan', 21))
        self.assertTrue(self.is_all_users_in_database([
            User(name='jo', age=20),
            User(name='alan', age=21),
        ]))
        
    def test_wrong_parameters(self):
        response = self.client.post('/users/', {
        })
        self.assertTrue(self.has_error_in_response(response))
        self.assertTrue(self.is_all_users_in_database([]))

        response = self.client.post('/users/', {
            'name': 'jo',
            'age': True,
        })
        self.assertTrue(self.has_error_in_response(response))
        self.assertTrue(self.is_all_users_in_database([]))

        response = self.client.post('/users/', {
            'name': 'jo',
        })
        self.assertTrue(self.has_error_in_response(response))
        self.assertTrue(self.is_all_users_in_database([]))
        
        response = self.client.post('/users/', {
            'age': 20,
        })
        self.assertTrue(self.has_error_in_response(response))
        self.assertTrue(self.is_all_users_in_database([]))

class TestPatchMethod(TestUsersView):

    def test_normal(self):
        user = User(name='jo', age=20)
        user.save()

        response = self.client.patch(f'/users/?id={user.id}', { # type: ignore
            'name': 'alan',
            'age': 22,
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.is_user_valid(response.json(), 'alan', 22))
        self.assertTrue(self.is_all_users_in_database([
            User(name='alan', age=22),
        ]))

        response = self.client.patch(f'/users/?id={user.id}', { # type: ignore
            '_id': self.fake_user_id,
            'id': self.fake_user_id,
            'fake': 'fake',
            'age': 21,
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertNotEqual(data['id'], self.fake_user_id)
        self.assertTrue(self.is_user_valid(data, 'alan', 21))
        self.assertTrue(self.is_all_users_in_database([
            User(name='alan', age=21),
        ]))
        
    def test_empty_parameters(self):
        user = User(name='jo', age=20)
        user.save()

        response = self.client.patch(f'/users/?id={user.id}', { # type: ignore
        })
        self.assertTrue(self.has_error_in_response(response))
        self.assertTrue(self.is_all_users_in_database([user]))
        
    def test_fake_user_id(self):
        user = User(name='jo', age=20)
        user.save()

        response = self.client.patch(f'/users/?id={self.fake_user_id}', { # type: ignore
            'name': 'alan',
            'age': 21,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)
        self.assertTrue(self.is_all_users_in_database([user]))

class TestPutMethod(TestUsersView):

    def test_normal(self):
        user = User(name='jo', age=20)
        user.save()

        response = self.client.put(f'/users/?id={user.id}', { # type: ignore
            'name': 'alan',
            'age': 20,
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.is_user_valid(response.json(), 'alan', 20))
        self.assertTrue(self.is_all_users_in_database([
            User(name='alan', age=20),
        ]))
        
        response = self.client.put(f'/users/?id={user.id}', { # type: ignore
            '_id': self.fake_user_id,
            'id': self.fake_user_id,
            'fake': 'fake',
            'name': 'alan',
            'age': 21,
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertNotEqual(data['id'], self.fake_user_id)
        self.assertTrue(self.is_user_valid(data, 'alan', 21))
        self.assertTrue(self.is_all_users_in_database([
            User(name='alan', age=21),
        ]))
        
    def test_idempotent(self):
        users = [
            User(name='jo', age=20),
            User(name='alan', age=21),
        ]
        self.create_users_to_database(users)
        
        self.client.put(f'/users/?id={users[0].id}', { # type: ignore
            'name': 'john',
            'age': 20,
        }, content_type='application/json')
        self.assertTrue(self.is_all_users_in_database([
            User(name='john', age=20),
            User(name='alan', age=21),
        ]))
        
        self.client.put(f'/users/?id={users[0].id}', { # type: ignore
            'name': 'john',
            'age': 20,
        }, content_type='application/json')
        self.assertTrue(self.is_all_users_in_database([
            User(name='john', age=20),
            User(name='alan', age=21),
        ]))

    def test_wrong_parameters(self):
        user = User(name='jo', age=20)
        user.save()

        response = self.client.put(f'/users/?id={user.id}', { # type: ignore
        }, content_type='application/json')
        self.assertTrue(self.has_error_in_response(response))
        self.assertTrue(self.is_all_users_in_database([user]))

        response = self.client.put(f'/users/?id={user.id}', { # type: ignore
            'age': 21,
        }, content_type='application/json')
        self.assertTrue(self.has_error_in_response(response))
        self.assertTrue(self.is_all_users_in_database([user]))
        
        response = self.client.put(f'/users/?id={user.id}', { # type: ignore
            'name': 'alan',
            'age': True,
        }, content_type='application/json')
        self.assertTrue(self.has_error_in_response(response))
        self.assertTrue(self.is_all_users_in_database([user]))
        
    def test_fake_user_id(self):
        user = User(name='jo', age=20)
        user.save()

        response = self.client.put(f'/users/?id={self.fake_user_id}', { # type: ignore
            'name': 'alan',
            'age': 21,
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)
        self.assertTrue(self.is_all_users_in_database([user]))

class TestDeleteMethod(TestUsersView):

    def test_normal(self):
        user = User(name='jo', age=20)
        user.save()

        response = self.client.delete(f'/users/?id={user.id}') # type: ignore
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.is_user_valid(response.json(), 'jo', 20))
        self.assertTrue(self.is_all_users_in_database([]))

    def test_idempotent(self):
        users = [
            User(name='jo', age=20),
            User(name='alan', age=21),
        ]
        self.create_users_to_database(users)
        
        self.client.delete(f'/users/?id={users[0].id}') # type: ignore
        self.assertTrue(self.is_all_users_in_database([users[1]]))
        
        self.client.delete(f'/users/?id={users[0].id}') # type: ignore
        self.assertTrue(self.is_all_users_in_database([users[1]]))
        
    def test_fake_user_id(self):
        user = User(name='jo', age=20)
        user.save()

        response = self.client.delete(f'/users/?id={self.fake_user_id}') # type: ignore
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)
        self.assertTrue(self.is_all_users_in_database([user]))
    