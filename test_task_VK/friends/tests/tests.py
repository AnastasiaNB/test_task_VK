import json
import os

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from friends.models import Status, User
from friends.serializers import CustomUserSerializer
from test_task_VK.settings import BASE_DIR


class UsersTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open(
            os.path.join(BASE_DIR, 'data/status.json'),
            encoding='utf-8'
        ) as data:
            statuses = json.loads(data.read())
            for status_item in statuses:
                Status.objects.get_or_create(**status_item)
        data = [{
            'username': 'name1',
            'email': 'name1@mail.ru',
            'password': 'password12345678'
        }, {
            'username': 'name2',
            'email': 'name2@mail.ru',
            'password': 'password12345678'
        }]
        for item in data:
            serializer = CustomUserSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        user_1 = User.objects.get(username='name1')
        user_2 = User.objects.get(username='name2')
        cls.auth_client_1 = APIClient()
        cls.auth_client_1.force_authenticate(user=user_1)
        cls.auth_client_2 = APIClient()
        cls.auth_client_2.force_authenticate(user=user_2)
        cls.client = APIClient()

    def test_create_user(self):
        url = '/api/users/'
        data = {
            'username': 'name3',
            'email': 'name3@mail.ru',
            'password': 'password12345678'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(id=2).username, 'name2')
        data = {
            'username': 'name3',
            'email': 'name3@mail.ru',
            'password': 'password12345678'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_users(self):
        urls = ['/api/users/', '/api/users/2/', '/api/users/me/']
        for url in urls:
            response = self.auth_client_1.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            if url == '/api/users/':
                self.assertEqual(len(response.data), 2)
            elif url == '/api/users/2/':
                self.assertEqual(response.data.get('username'), 'name2')
            else:
                self.assertEqual(response.data.get('username'), 'name1')
            response = self.client.get(url, format='json')
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED
            )

    def test_friend_requests(self):
        urls = [
            '/api/friends/2/', '/api/users/i_follow/',
            '/api/users/my_followers/', '/api/users/my_friends/'
        ]
        for url in urls:
            if url == '/api/friends/2/':
                response = self.client.post(url, format='json')
            else:
                response = self.client.get(url, format='json')
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED
            )
        response = self.auth_client_1.post('/api/friends/2/', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.auth_client_1.post('/api/friends/2/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.auth_client_1.post('/api/friends/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.auth_client_1.get(
            '/api/users/i_follow/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get('username'), 'name2')
        self.assertEqual(response.data[0].get('status'), 'I follow')
        response = self.auth_client_2.get(
            '/api/users/my_followers/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get('username'), 'name1')
        self.assertEqual(response.data[0].get('status'), 'My follower')
        self.auth_client_2.post('/api/friends/1/', format='json')
        response = self.auth_client_2.get(
            '/api/users/my_followers/',
            format='json'
        )
        self.assertEqual(len(response.data), 0)
        response = self.auth_client_2.get(
            '/api/users/my_friends/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get('username'), 'name1')
        self.assertEqual(response.data[0].get('status'), 'friend')
        response = self.auth_client_1.get(
            '/api/users/my_friends/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get('username'), 'name2')
        self.assertEqual(response.data[0].get('status'), 'friend')
        self.auth_client_2.delete('/api/friends/1/', format='json')
        response = self.auth_client_2.get(
            '/api/users/my_followers/',
            format='json'
        )
        self.assertEqual(len(response.data), 1)
