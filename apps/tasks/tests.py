"""Task endpoints tests"""
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
    """TestTask"""
    queryset = Task.objects.all()

    def setUp(self) -> None:
        """TestTask"""
        self.user = User.objects.filter(email='condrealili12@gmail.com')
        self.client.force_authenticate(self.user)

    def test_get(self):
        """TestTask"""
        response = self.client.get(reverse('tasks_list'),
                                   params=(title_random,))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        """TestTask"""
        response = self.client.post(reverse('tasks_list'),
                                    data=task_fake_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_top_20(self):
        """TestTask"""
        response = self.client.get(reverse('tasks_top_20'),
                                   params=(title_random,))
        self.assertEqual(response.status_code, 200)

    def test_get_by_pk(self):
        """TestTask"""
        response = self.client.get(reverse('tasks_detail',
                                           args=(id_random,)))
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        """TestTask"""
        response = self.client.put(reverse('tasks_detail', args=(id_random,)),
                                   data=task_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch(self):
        """TestTask"""
        response = self.client.patch(reverse('tasks_detail', args=(id_random,)),
                                     data=task_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        """TestTask"""
        response = self.client.delete(reverse('tasks_detail', args=(id_random,)))
        self.assertEqual(response.status_code, 200)

    def test_get_comments(self):
        """TestTask"""
        response = self.client.get(reverse('tasks_comments_list', args=(id_random,)))
        self.assertEqual(response.status_code, 200)

    def test_get_timelogs(self):
        """TestTask"""
        response = self.client.get(reverse('tasks_logs_list', args=(id_random,)))
        self.assertEqual(response.status_code, 200)

    def test_update_owner(self):
        """TestTask"""
        fake_data = {
            "owner": random.choice(User.objects.all()).id,
        }
        response = self.client.patch(reverse('tasks_update_owner', args=(id_random,)),
                                     data=fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_status(self):
        """TestTask"""
        fake_data = {
            "status": faker.boolean(),
        }
        response = self.client.patch(reverse('tasks_update_status', args=(id_random,)),
                                     data=fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_users(self):
        """TestTask"""
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)


comment_fake_data = {
    "task": random.choice(Task.objects.all()).id,
    "text": faker.text(),
}
random_id = random.choice(Comment.objects.all()).id


class TestComment(APITestCase):
    """TestComment"""
    queryset = Comment.objects.all()

    def setUp(self) -> None:
        """TestComment"""
        self.user = User.objects.filter(email='condrealili12@gmail.com')
        self.client.force_authenticate(self.user)

    def test_get(self):
        """TestComment"""
        response = self.client.get(reverse('comments_list'))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        """TestComment"""
        response = self.client.post(reverse('comments_list'), data=comment_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_by_pk(self):
        """TestComment"""
        response = self.client.get(reverse('comments_detail', args=(random_id,)))
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """TestComment"""
        response = self.client.put(reverse('comments_detail', args=(random_id,)),
                                   data=comment_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        """TestComment"""
        response = self.client.patch(reverse('comments_detail', args=(random_id,)),
                                     data=comment_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        """TestComment"""
        self.client.delete(reverse('comments_detail', args=(random_id,)))
        self.assertEqual(self.queryset.filter(pk=random_id).count(), 0)
