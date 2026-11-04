from django.test import TestCase
from django.urls import reverse

from issue_tracker.models import Status, Task, Type


class TaskFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.status = Status.objects.create(status_name='New')
        cls.task_type = Type.objects.create(type_name='Task')
        cls.task = Task.objects.create(
            summary='Исходная задача', status=cls.status, type=cls.task_type,
        )

    def form_data(self, summary):
        return {
            'summary': summary, 'description': 'Описание',
            'status': self.status.pk, 'type': self.task_type.pk,
        }

    def test_navigation_and_edit_links(self):
        create_url = reverse('tasks_create')
        update_url = reverse('tasks_update', args=[self.task.pk])
        for url in (reverse('tasks_list'), reverse('tasks_detail', args=[self.task.pk])):
            response = self.client.get(url)
            self.assertContains(response, f'href="{create_url}"')
            self.assertContains(response, f'href="{update_url}"')
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, f'href="{create_url}"')
        response = self.client.get(update_url)
        self.assertContains(response, self.task.summary)
        self.assertContains(response, f'href="{create_url}"')

    def test_create_task(self):
        response = self.client.post(reverse('tasks_create'), self.form_data('Новая задача'))
        task = Task.objects.get(summary='Новая задача')
        self.assertRedirects(response, reverse('tasks_detail', args=[task.pk]))

    def test_update_task(self):
        response = self.client.post(
            reverse('tasks_update', args=[self.task.pk]), self.form_data('Изменённая задача'),
        )
        self.assertRedirects(response, reverse('tasks_detail', args=[self.task.pk]))
        self.task.refresh_from_db()
        self.assertEqual(self.task.summary, 'Изменённая задача')
        self.assertEqual(Task.objects.count(), 1)

    def test_invalid_forms(self):
        for url in (reverse('tasks_create'), reverse('tasks_update', args=[self.task.pk])):
            response = self.client.post(url, self.form_data(''))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
        self.task.refresh_from_db()
        self.assertEqual(self.task.summary, 'Исходная задача')
        self.assertEqual(Task.objects.count(), 1)

    def test_missing_task(self):
        self.assertEqual(self.client.get(reverse('tasks_update', args=[999])).status_code, 404)
