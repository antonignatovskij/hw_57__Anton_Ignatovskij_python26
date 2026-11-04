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

class Type(models.Model):
    type_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f'type:{self.pk} - {self.type_name}'

    class Meta:
        db_table = "type"
        verbose_name = "тип"

class Status(models.Model):
    status_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f'status:{self.pk} - {self.status_name}'

    class Meta:
        db_table = "status"
        verbose_name = "статус"


