from django.db import models

# Create your models here.

class Task(models.Model):
    summary = models.CharField(max_length=100, null=False, blank=False, verbose_name="Заголовок")
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name="Описание")

    status = models.ForeignKey(
        'issue_tracker.Status',
        related_name='tasks',
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
        verbose_name="Статус",
        default=1,
    )

    types = models.ManyToManyField(
        'issue_tracker.Type',
        related_name='tasks',
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'task:{self.pk} - {self.summary[:40]}'

    class Meta:
        db_table = "task"
        verbose_name = "задача"