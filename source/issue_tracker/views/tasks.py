from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from issue_tracker.forms import TaskForm
from issue_tracker.models import Project, Status, Task


class TaskDetailView(DetailView):
    queryset = Task.objects.select_related('project', 'status').prefetch_related('types')
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskCreationView(PermissionRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    permission_required = 'issue_tracker.add_task'

    def has_permission(self) -> bool:
        return super().has_permission() and self.request.user in self.project.members.all()

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
        return reverse('issue_tracker:tasks_detail', kwargs={'pk': self.object.pk})


class TaskUpdateView(PermissionRequiredMixin, UpdateView):
    queryset = Task.objects.select_related('project')
    form_class = TaskForm
    template_name = 'tasks/update.html'
    context_object_name = 'task'
    permission_required = 'issue_tracker.change_task'

    def has_permission(self) -> bool:
        return super().has_permission() and self.request.user in self.get_object().project.members.all()

    def get_success_url(self):
        return reverse('issue_tracker:tasks_detail', kwargs={'pk': self.object.pk})


class TaskDeleteView(PermissionRequiredMixin, DeleteView):
    queryset = Task.objects.select_related('project')
    template_name = 'tasks/delete.html'
    context_object_name = 'task'
    permission_required = 'issue_tracker.delete_task'

    def has_permission(self) -> bool:
        return super().has_permission() and self.request.user in self.get_object().project.members.all()

    def get_success_url(self):
        return reverse('issue_tracker:projects_detail', kwargs={'pk': self.object.project_id})
