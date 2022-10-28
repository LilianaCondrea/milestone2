from django.db import models

from ..tasks.models import Task
from ..users.models import User


# Create your models here.
class TimeLog(models.Model):
    start_timer = models.DateTimeField(null=True)
    end_timer = models.DateTimeField(null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
