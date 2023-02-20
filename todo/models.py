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
    name = models.CharField(max_length=50)
    description = models.TextField()
    start_time = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    finish_time = models.DateTimeField
    project_id = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks_as_author",
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subtask_as_executor",
    )
    is_done = models.BooleanField(default=False)


class SubTask(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    # start_time = models.DateTimeField(auto_now=True)
    # deadline = models.DateTimeField()
    # finish_time = models.DateTimeField
    project_id = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_of_subtask",
    )
    task_id = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="task_of_subtask",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subtasks_as_author",
    )
    is_done = models.BooleanField(default=False)