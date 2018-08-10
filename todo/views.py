from django.shortcuts import render
from django.http import HttpResponse
from .models import TaskModel
from django.utils import timezone

def index(request):
    return HttpResponse("Hello, world. You're at the todo index.")

def upcoming(request):
    upcoming_task_list = TaskModel.objects.filter(due_date__gte=timezone.now().strftime("%Y-%m-%d %H:%M:%S"))[:5]
    output = ', '.join([t.title for t in upcoming_task_list])
    return HttpResponse(output)
