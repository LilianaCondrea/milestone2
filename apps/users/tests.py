from django.urls import reverse

from faker import Faker
from rest_framework.test import APITestCase
from .models import User

faker = Faker()


# User endpoints unit tests
class TestUser(APITestCase):
    queryset = User.objects.all()

    def setUp(self) -> None:
        self.user = User.objects.all()
        self.client.force_authenticate(self.user)

    def test_register(self):
        fake_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "password": faker.password(),
        }
        response = self.client.post(reverse('register'), data=fake_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_auth(self):
        fake_data = {
            "email": 'condrealili12@gmail.com',
            "password": 'admin',
        }
        response = self.client.post(reverse('token_obtain_pair'), data=fake_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_token_refresh(self):
        fake_data = {
            "refresh": faker.password(),
        }
        token = self.client.post(reverse('token_obtain_pair'), data={"email": 'condrealili12@gmail.com',
                                                                     "password": 'admin'}, format='json').json()
        response = self.client.post(reverse('token_refresh'), data=fake_data, format='json')
        self.assertEqual(response.status_code, 401)
