from django.db import models

# Create your models here.

class Task(models.Model):
    summary = models.CharField(max_length=100, null=False, blank=False, verbose_name="Заголовок")
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name="Описание")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'task:{self.pk} - {self.summary[:40]}'

    class Meta:
        db_table = "task"
        verbose_name = "задача"