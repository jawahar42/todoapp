from tastypie.resources import ModelResource
from todo.models import TaskModel


class TaskModelResource(ModelResource):
    class Meta:
        queryset = TaskModel.objects.all()
        allowed_methods = ['get', 'post']