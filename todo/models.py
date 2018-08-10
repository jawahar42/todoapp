from django.db import models

class TaskModel(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True)
    due_date = models.DateTimeField()
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
