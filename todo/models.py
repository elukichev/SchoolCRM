from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    start_time = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    finish_time = models.DateTimeField
    is_done = models.BooleanField(default=False)
    users = models.ManyToManyField(User)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="project_as_author",
    )
    executors = models.ManyToManyField(
        User,
        related_name="project_as_executor",
    )


class Task(models.Model):
    description = models.TextField()
    start_time = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    finish_time = models.DateTimeField
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks_as_author",
    )
    executors = models.ManyToManyField(
        User,
        related_name="tasks_as_executor",
    )
    is_done = models.BooleanField(default=False)
