import random

from django.core.management import BaseCommand
from faker import Faker

from ....tasks.models import Task
from ....users.models import User

faker = Faker()


class Command(BaseCommand):
    help = 'Generate tasks'

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int, help='amount of tasks to generate')

    def handle(self, *args, **options):
        count = 0
        for _ in range(50):
            task = Task.objects.create(
                title=faker.unique.name(),
                description=faker.text(),
                status=faker.boolean(),
                owner=random.choice(User.objects.all())
            )
            count += 1
            print('Task ' + str(task.title) + ' generated:' + str(count))
            print('were generated ' + str(count) + ' tasks')
