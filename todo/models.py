from django.db import models

class TaskModel(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, default=None)
    due_date = models.DateTimeField()
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
