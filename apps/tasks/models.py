from django.db import models

from ..users.models import User


class Task(models.Model):
    title = models.CharField(db_index=True, max_length=100)
    description = models.TextField()
    status = models.BooleanField(db_index=True, default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=True, db_constraint=False)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_index=True)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
