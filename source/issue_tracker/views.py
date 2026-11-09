from typing import Any

from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, FormView

from issue_tracker.forms import TaskForm
from issue_tracker.models import Task, Status



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


# class TaskCreationView(View):
#     def get(self, request, *args, **kwargs):
#         try:
#             new_status = Status.objects.get(status_name='New')
#             form = TaskForm(initial={'status': new_status.pk})
#             return render(request, 'tasks/create.html', {'form': form})
#         except Status.DoesNotExist:
#             form = TaskForm()
#             return render(request, 'tasks/create.html', {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save()
#             task.types.set(form.cleaned_data['types'])
#             task.save()
#             return redirect('tasks_detail', pk=task.pk)
#         return render(request, 'tasks/create.html', {'form': form})

class TaskCreationView(FormView):
    form_class = TaskForm
    template_name = "tasks/create.html"

    def get_initial(self):
        initial = super().get_initial()
        try:
            new_status = Status.objects.get(status_name='New')
            initial['status'] = new_status.pk
        except Status.DoesNotExist:
            pass
        return initial

    def form_valid(self, form):
        summary = form.cleaned_data['summary']
        description = form.cleaned_data['description']
        status = form.cleaned_data['status']
        types = form.cleaned_data.pop('types')
        task = Task.objects.create(summary=summary, description=description, status=status)
        task.types.set(types)
        task.save()
        return redirect('tasks_detail', pk=task.pk)



# class TaskUpdateView(View):
#     def dispatch(self, request, *args, **kwargs):
#         self.task = get_object_or_404(Task, pk=kwargs.get('pk'))
#         return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         form = TaskForm(instance=self.task)
#         context = {'form': form, 'task': self.task}
#         return render(request, 'tasks/update.html', context)
#
#     def post(self, request, *args, **kwargs):
#         form = TaskForm(request.POST, instance=self.task)
#         if form.is_valid():
#             task = form.save()
#             task.types.set(form.cleaned_data['types'])
#             task.save()
#             return redirect('tasks_detail', pk=task.pk)
#         return render(request, 'tasks/update.html', {'form': form, 'task': self.task})

class TaskUpdateView(FormView):
    template_name = 'tasks/update.html'
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        form = TaskForm(instance=task)
        context['form'] = form
        context['task'] = task
        return context

    def form_valid(self, form):
        types = form.cleaned_data.pop('types')
        task = Task.objects.get(pk=self.kwargs['pk'])
        for key, value in form.cleaned_data.items():
            if value is not None:
                setattr(task, key, value)
        task.save()
        task.types.set(types)
        return redirect('tasks_detail', pk=task.pk)




class TaskDeleteView(View):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        task.delete()
        return redirect('tasks_list')