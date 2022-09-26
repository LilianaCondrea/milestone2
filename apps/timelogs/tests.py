import random

from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from .models import TimeLog
from ..tasks.models import Task
from ..users.models import User

faker = Faker()
timelog_fake_data = {
    "start_timer": faker.date_time_this_year(),
    "end_timer": faker.date_time_this_year(),
    "task": random.choice(Task.objects.all()).id,
    "owner": random.choice(User.objects.all()).id
}
id_random = random.choice(Task.objects.all()).id


class TestTimeLog(APITestCase):
    queryset = TimeLog.objects.all()

    def setUp(self) -> None:
        self.user = User.objects.filter(email='condrealili12@gmail.com')
        self.client.force_authenticate(self.user)

    def test_get(self):
        response = self.client.get(reverse('timelogs_list'))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(reverse('timelogs_list'), data=timelog_fake_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_start_timer(self):
        fake_data = {
            "task": random.choice(Task.objects.all()).id
        }
        response = self.client.post(reverse('timelogs_start'), data=fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_end_timer(self):
        fake_data = {
            "task": random.choice(Task.objects.all()).id
        }
        response = self.client.post(reverse('timelogs_stop'), data=fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_by_pk(self):
        response = self.client.get(reverse('timelogs-detail', args=(id_random,)))
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        response = self.client.put(reverse('timelogs-detail', args=(id_random,)), data=timelog_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch(self):
        response = self.client.patch(reverse('timelogs-detail', args=(id_random,)), data=timelog_fake_data,
                                     format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.delete(reverse('timelogs-detail', args=(id_random,)))
        self.assertEqual(self.queryset.filter(pk=id_random).count(), 0)
