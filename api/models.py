from django.db import models
from django.conf import settings
import datetime


User = settings.AUTH_USER_MODEL
# Create your models here.


class TaskModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    due_date = models.DateField(default=datetime.date.today)


class SubTaskModel(models.Model):
    task = models.ForeignKey(TaskModel, related_name="subtasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    due_date = models.DateField(default=datetime.date.today)
    assigned_to = models.CharField(default=1, max_length=200)

class CollaboratorModel(models.Model):
    username = models.CharField(max_length=200)
    task = models.ForeignKey(TaskModel, related_name="collaborators", on_delete=models.CASCADE)