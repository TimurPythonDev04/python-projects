from django.db import models
from django.contrib.auth.models import User


class Task(models.Model) :
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField( null = True ,blank=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
# Create your models here.
