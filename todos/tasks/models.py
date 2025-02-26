from django.db import models
from authentication.models import User

class TaskStatus(models.IntegerChoices):
    OPEN = 0, 'Open'
    COMPLETED = 1, 'Completed'

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(
        choices=TaskStatus.choices,
        default=TaskStatus.OPEN,
    )

    def __str__(self):
        return self.title
