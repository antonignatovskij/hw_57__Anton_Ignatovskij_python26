from datetime import date
from urllib.parse import urlencode

from django.test import TestCase
from django.urls import reverse

from issue_tracker.models import Project, Status, Task, Type


class ProjectViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(
            name='Основной проект', description='Полное описание основного проекта',
            beginning_date=date(2026, 1, 2), ending_date=date(2026, 12, 31),
        )
        cls.other_project = Project.objects.create(
            name='Другой проект', description='Описание другого проекта',
            beginning_date=date(2026, 2, 1),
        )
        cls.status = Status.objects.create(status_name='New')
        cls.task_type = Type.objects.create(type_name='Task')
        cls.task = Task.objects.create(
            summary='Задача основного проекта', description='Полное описание задачи',
            status=cls.status, project=cls.project,
        )
        cls.task.types.add(cls.task_type)
        cls.other_task = Task.objects.create(
            summary='Задача другого проекта', status=cls.status, project=cls.other_project,
        )

    def project_data(self, **overrides):
        data = {
            'name': 'Новый проект', 'description': 'Описание нового проекта',
            'beginning_date': '2026-03-01', 'ending_date': '',
        }
        data.update(overrides)
        return data

    def test_homepage_search_and_pagination(self):
        for number in range(12):
            Project.objects.create(
                name=f'Page & Project {number}', description='Описание проекта',
                beginning_date=date(2026, 3, 1),
            )
        self.assertEqual(reverse('projects_list'), '/')
        seen = set()
        for page, count in [(1, 5), (2, 5), (3, 2)]:
            response = self.client.get('/', {'search': 'Page & Project', 'page': page})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context['projects']), count)
            seen.update(project.pk for project in response.context['projects'])
            self.assertEqual(response.context['paginator'].num_pages, 3)
        self.assertEqual(len(seen), 12)
        response = self.client.get('/', {'search': 'Page & Project'})
        query = urlencode({'search': 'Page & Project'})
        self.assertContains(response, f'href="?{query}&amp;page=2"')
        self.assertContains(response, 'name="search" value="Page &amp; Project"')
        self.assertContains(response, 'name="page"')

    def test_search_by_name_or_description(self):
        self.project.name = 'NameMarker'
        self.project.save()
        self.other_project.description = 'DescriptionMarker'
        self.other_project.save()
        for query, expected in [('namemarker', self.project), ('descriptionmarker', self.other_project)]:
            with self.subTest(query=query):
                response = self.client.get('/', {'search': f'  {query}  '})
                self.assertEqual(list(response.context['projects']), [expected])
                self.assertTrue(response.context['form'].is_valid())

    def test_empty_search_result_keeps_form(self):
        response = self.client.get('/', {'search': 'NoMatchingProjectAnywhere'})
        self.assertContains(response, 'Проекты не найдены')
        self.assertContains(response, 'name="search"')
        self.assertNotContains(response, 'aria-label="Пагинация"')

    def test_invalid_search_shows_form_error(self):
        response = self.client.get('/', {'search': 'x' * 101})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].has_error('search', 'max_length'))
        self.assertContains(response, 'value="' + 'x' * 101 + '"')

    def test_detail_shows_only_project_tasks_and_actions(self):
        response = self.client.get(reverse('projects_detail', args=[self.project.pk]))
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.task.summary)
        self.assertNotContains(response, self.other_task.summary)
        for name in ('tasks_detail', 'tasks_update', 'tasks_delete'):
            self.assertContains(response, reverse(name, args=[self.task.pk]))
        self.assertContains(response, reverse('tasks_create', args=[self.project.pk]))
        self.assertContains(response, reverse('projects_update', args=[self.project.pk]))
        self.assertContains(response, reverse('projects_delete', args=[self.project.pk]))

    def test_create_project_with_optional_end_date(self):
        response = self.client.post(reverse('projects_create'), self.project_data())
        project = Project.objects.get(name='Новый проект')
        self.assertEqual(project.beginning_date, date(2026, 3, 1))
        self.assertIsNone(project.ending_date)
        self.assertRedirects(response, reverse('projects_detail', args=[project.pk]))

    def test_project_date_inputs_and_edit(self):
        url = reverse('projects_update', args=[self.project.pk])
        response = self.client.get(url)
        self.assertContains(response, 'type="date"', count=2)
        self.assertContains(response, 'value="2026-01-02"')
        response = self.client.post(url, self.project_data(name='Обновлённый проект'))
        self.assertRedirects(response, reverse('projects_detail', args=[self.project.pk]))
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Обновлённый проект')
        self.assertIsNone(self.project.ending_date)

    def test_invalid_project_form_preserves_input(self):
        response = self.client.post(
            reverse('projects_create'), self.project_data(beginning_date='bad-date'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('beginning_date', response.context['form'].errors)
        self.assertContains(response, 'value="Новый проект"')
        self.assertFalse(Project.objects.filter(name='Новый проект').exists())

    def test_project_end_date_cannot_precede_start(self):
        response = self.client.post(
            reverse('projects_create'), self.project_data(ending_date='2026-02-01'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(Project.objects.filter(name='Новый проект').exists())

    def test_project_delete_requires_post_and_removes_only_its_tasks(self):
        url = reverse('projects_delete', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        response = self.client.post(url)
        self.assertRedirects(response, reverse('projects_list'))
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        self.assertTrue(Task.objects.filter(pk=self.other_task.pk).exists())

    def test_missing_projects_return_404(self):
        for name in ('projects_detail', 'projects_update', 'projects_delete'):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name, args=[999999])).status_code, 404)


class TaskFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.status = Status.objects.create(status_name='New')
        cls.task_type = Type.objects.create(type_name='Task')
        cls.other_type = Type.objects.create(type_name='Bug')
        cls.project = Project.objects.create(
            name='Проект задачи', description='Описание проекта', beginning_date=date(2026, 1, 1),
        )
        cls.other_project = Project.objects.create(
            name='Другой проект', description='Другой проект', beginning_date=date(2026, 1, 1),
        )
        cls.task = Task.objects.create(
            summary='Исходная задача', description='Описание исходной задачи',
            status=cls.status, project=cls.project,
        )
        cls.task.types.add(cls.task_type)

    def form_data(self, summary, **overrides):
        data = {
            'summary': summary, 'description': 'Полное описание задачи',
            'status': self.status.pk, 'types': [self.task_type.pk],
        }
        data.update(overrides)
        return data

    def test_navigation_and_project_is_not_a_form_field(self):
        create_url = reverse('tasks_create', args=[self.project.pk])
        for url in (reverse('tasks_detail', args=[self.task.pk]), reverse('tasks_update', args=[self.task.pk])):
            response = self.client.get(url)
            self.assertContains(response, reverse('projects_detail', args=[self.project.pk]))
            self.assertNotContains(response, 'name="project"')
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('project', response.context['form'].fields)
        self.assertNotContains(response, 'name="project"')
        self.assertEqual(response.context['form'].initial['status'], self.status.pk)

    def test_create_task_uses_project_from_url_and_saves_types(self):
        response = self.client.post(
            reverse('tasks_create', args=[self.project.pk]),
            self.form_data('Новая задача', project=self.other_project.pk),
        )
        task = Task.objects.get(summary='Новая задача')
        self.assertRedirects(response, reverse('tasks_detail', args=[task.pk]))
        self.assertEqual(task.project_id, self.project.pk)
        self.assertEqual(list(task.types.all()), [self.task_type])

    def test_update_task_preserves_project_and_updates_types(self):
        response = self.client.post(
            reverse('tasks_update', args=[self.task.pk]),
            self.form_data('Изменённая задача', types=[self.other_type.pk], project=self.other_project.pk),
        )
        self.assertRedirects(response, reverse('tasks_detail', args=[self.task.pk]))
        self.task.refresh_from_db()
        self.assertEqual(self.task.summary, 'Изменённая задача')
        self.assertEqual(self.task.project_id, self.project.pk)
        self.assertEqual(list(self.task.types.all()), [self.other_type])
        self.assertEqual(Task.objects.count(), 1)

    def test_invalid_forms_keep_errors_input_and_project(self):
        for url in (reverse('tasks_create', args=[self.project.pk]), reverse('tasks_update', args=[self.task.pk])):
            with self.subTest(url=url):
                response = self.client.post(url, self.form_data('Коротко'))
                self.assertEqual(response.status_code, 200)
                self.assertIn('summary', response.context['form'].errors)
                self.assertContains(response, 'value="Коротко"')
                self.assertContains(response, reverse('projects_detail', args=[self.project.pk]))
        self.task.refresh_from_db()
        self.assertEqual(self.task.summary, 'Исходная задача')
        self.assertEqual(Task.objects.count(), 1)

    def test_delete_task_returns_to_its_project(self):
        url = reverse('tasks_delete', args=[self.task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        response = self.client.post(url)
        self.assertRedirects(response, reverse('projects_detail', args=[self.project.pk]))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_missing_task_and_missing_parent_project(self):
        for name in ('tasks_detail', 'tasks_update', 'tasks_delete'):
            self.assertEqual(self.client.get(reverse(name, args=[999999])).status_code, 404)
        url = reverse('tasks_create', args=[999999])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.post(url, self.form_data('Новая задача')).status_code, 404)
        self.assertEqual(Task.objects.count(), 1)

    def test_old_global_task_routes_are_removed(self):
        for url in ('/tasks/', '/tasks/create/'):
            self.assertEqual(self.client.get(url).status_code, 404)
            self.assertEqual(self.client.post(url, self.form_data('Новая задача')).status_code, 404)
