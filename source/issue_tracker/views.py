from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from issue_tracker.forms import TaskForm
from issue_tracker.models import Task


# Create your views here.

class TasksView(TemplateView):
    template_name = "tasks/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context



class TaskDetailView(TemplateView):
    template_name = "tasks/detail.html"

    def get_context_data(self, **kwargs):
        kwargs['task'] = get_object_or_404(Task, pk=self.kwargs['pk'])
        return super().get_context_data(**kwargs)


class TaskCreationView(View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'tasks/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('tasks_detail', pk=task.pk)
        return render(request, 'tasks/create.html', {'form': form})

class TaskUpdateView(View):
    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TaskForm(instance=self.task)
        context = {'form': form, 'task': self.task}
        return render(request, 'tasks/update.html', context)

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST, instance=self.task)
        if form.is_valid():
            task = form.save()
            return redirect('tasks_detail', pk=task.pk)
        return render(request, 'tasks/update.html', {'form': form, 'task': self.task})

class TaskDeleteView(View):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        task.delete()
        return redirect('tasks_list')