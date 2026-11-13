from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from issue_tracker.forms import TaskForm
from issue_tracker.models import Project, Status, Task


class TaskDetailView(DetailView):
    queryset = Task.objects.select_related('project', 'status').prefetch_related('types')
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskCreationView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['project_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        new_status = Status.objects.filter(status_name='New').first()
        if new_status is not None:
            initial['status'] = new_status.pk
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tasks_detail', kwargs={'pk': self.object.pk})


class TaskUpdateView(UpdateView):
    queryset = Task.objects.select_related('project')
    form_class = TaskForm
    template_name = 'tasks/update.html'
    context_object_name = 'task'

    def get_success_url(self):
        return reverse('tasks_detail', kwargs={'pk': self.object.pk})


class TaskDeleteView(DeleteView):
    queryset = Task.objects.select_related('project')
    template_name = 'tasks/delete.html'
    context_object_name = 'task'

    def get_success_url(self):
        return reverse('projects_detail', kwargs={'pk': self.object.project_id})
