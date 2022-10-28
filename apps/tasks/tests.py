import random
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from .models import Task, Comment
from ..users.models import User

faker = Faker()
task_fake_data = {
    "title": faker.word(),
    "description": faker.text(),
    "status": faker.boolean(),
    "owner": random.choice(User.objects.all()).id,
}
id_random = random.choice(Task.objects.all()).id
title_random = random.choice(Task.objects.all()).title


# Task endpoints unit tests
class TestTask(APITestCase):
    queryset = Task.objects.all()

    def setUp(self) -> None:
        self.user = User.objects.filter(email='condrealili12@gmail.com')
        self.client.force_authenticate(self.user)

    def test_get(self):
        response = self.client.get(reverse('Tasks-list'),
                                   params=(title_random,))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(reverse('Tasks-list'),
                                    data=task_fake_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_top_20(self):
        response = self.client.get(reverse('Tasks-top-20'),
                                   params=(title_random,))
        self.assertEqual(response.status_code, 200)

    def test_get_by_pk(self):
        response = self.client.get(reverse('Tasks-detail',
                                           args=(id_random,)))
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        response = self.client.put(reverse('Tasks-detail', args=(id_random,)),
                                   data=task_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch(self):
        response = self.client.patch(reverse('Tasks-detail', args=(id_random,)),
                                     data=task_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_my_tasks(self):
        response = self.client.get(reverse('Tasks-my-tasks'))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.delete(reverse('Tasks-detail', args=(id_random,)))
        self.assertEqual(response.status_code, 200)

    def test_get_comments(self):
        response = self.client.get(reverse('task-comments', args=(id_random,)))
        self.assertEqual(response.status_code, 200)

    def test_get_timelogs(self):
        response = self.client.get(reverse('task-logs', args=(id_random,)))
        self.assertEqual(response.status_code, 200)

    def test_update_owner(self):
        fake_data = {
            "owner": random.choice(User.objects.all()).id,
        }
        response = self.client.patch(reverse('Tasks-update-owner', args=(id_random,)),
                                     data=fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_status(self):
        fake_data = {
            "status": faker.boolean(),
        }
        response = self.client.patch(reverse('Tasks-update-status', args=(id_random,)),
                                     data=fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_users(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)


comment_fake_data = {
    "task": random.choice(Task.objects.all()).id,
    "text": faker.text(),
}
random_id = random.choice(Comment.objects.all()).id


class TestComment(APITestCase):
    queryset = Comment.objects.all()

    def setUp(self) -> None:
        self.user = User.objects.filter(email='condrealili12@gmail.com')
        self.client.force_authenticate(self.user)

    def test_get(self):
        response = self.client.get(reverse('Comments-list'))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(reverse('Comments-list'), data=comment_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_by_pk(self):
        response = self.client.get(reverse('Comments-detail', args=(random_id,)))
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        response = self.client.put(reverse('Comments-detail', args=(random_id,)),
                                   data=comment_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        response = self.client.patch(reverse('Comments-detail', args=(random_id,)),
                                     data=comment_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.client.delete(reverse('Comments-detail', args=(random_id,)))
        self.assertEqual(self.queryset.filter(pk=random_id).count(), 0)
