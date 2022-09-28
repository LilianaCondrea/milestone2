import random

from django.core.management import BaseCommand
from faker import Faker

from ....tasks.models import Task
from ....timelogs.models import TimeLog
from ....users.models import User

faker = Faker()


class Command(BaseCommand):
    help = 'Generate timelogs'

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int, help='amount of timelogs to generate')

    def handle(self, *args, **options):
        count = 0
        for _ in range(50):
            random_task = random.choice(Task.objects.all())
            timelog = TimeLog.objects.create(
                start_timer=faker.past_datetime(),
                end_timer=faker.future_datetime(),
                task=random_task,
                owner=random_task.owner
            )
            count += 1
            print('TimeLog for ' + str(timelog.task) + ' generated:' + str(count))
            print('were generated ' + str(count) + ' timelogs')
