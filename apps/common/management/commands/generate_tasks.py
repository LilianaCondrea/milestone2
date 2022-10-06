import random

from django.core.management import BaseCommand
from faker import Faker

from ....tasks.models import Task
from ....timelogs.models import TimeLog
from ....users.models import User




class Command(BaseCommand):
    help = 'Generate tasks'

    # def add_arguments(self, parser):
    #     parser.add_argument('--amount', type=int, help='amount of tasks to generate')

    def handle(self, *args, **options):
        fake = Faker()
        owner = User.objects.get(pk=2)
        for i in range(25000):
            task = Task.objects.create(
                title=fake.unique.name(),
                description=fake.word(),
                status=fake.boolean(),
                owner=owner
            )
            task.save()

            timelog = TimeLog.objects.create(
                    start_timer=fake.past_datetime(),
                    end_timer=fake.future_datetime(),
                    task=task,
                    owner=owner
            )
            timelog.save()
            # count += 1
            # print('Task ' + str(task.title) + ' generated:' + str(count))
            # print('were generated ' + str(count) + ' tasks')
