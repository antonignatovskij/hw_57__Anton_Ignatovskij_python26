from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from issue_tracker.forms import ProjectForm, SimpleSearchForm, MemberAddForm, MemberDeleteForm
from issue_tracker.models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/index.html'
    context_object_name = 'projects'
    paginate_by = 5
    paginate_orphans = 1
    ordering = ('-beginning_date', '-pk')

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(name__icontains=self.search_value)
                | Q(description__icontains=self.search_value)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ProjectDetailView(DetailView):
    template_name = 'projects/detail.html'
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all().order_by('-created_at')
        return context


class ProjectCreationView(PermissionRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create.html'
    permission_required = 'issue_tracker.add_project'

    def form_valid(self, form):
        project = form.save()
        project.members.add(self.request.user)
        project.save()
        return super().form_valid(form)

    def has_permission(self) -> bool:
        return super().has_permission()

    def get_success_url(self):
        return reverse('issue_tracker:projects_detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/update.html'
    context_object_name = 'project'
    permission_required = 'issue_tracker.change_project'

    def has_permission(self) -> bool:
        return super().has_permission() and self.request.user in self.get_object().members.all()

    def get_success_url(self):
        return reverse('issue_tracker:projects_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('issue_tracker:projects_list')
    permission_required = 'issue_tracker.delete_project'

    def has_permission(self) -> bool:
        return super().has_permission() and self.request.user in self.get_object().members.all()


class ProjectMemberAddView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = MemberAddForm
    template_name = 'projects/members_update.html'
    context_object_name = 'project'
    permission_required = 'issue_tracker.can_add_member_to_project'

    def has_permission(self) -> bool:
        return super().has_permission() and self.request.user in self.get_object().members.all()

    def form_valid(self, form):
        self.object.members.add(*form.cleaned_data['members'])
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('issue_tracker:projects_detail', kwargs={'pk': self.object.pk})


class ProjectMemberDeleteView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = MemberDeleteForm
    template_name = 'projects/members_update.html'
    context_object_name = 'project'
    permission_required = 'issue_tracker.can_remove_member_of_project'

    def has_permission(self) -> bool:
        return super().has_permission() and self.request.user in self.get_object().members.all()

    def form_valid(self, form):
        self.object.members.remove(*form.cleaned_data['members'])
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('issue_tracker:projects_detail', kwargs={'pk': self.object.pk})