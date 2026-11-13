from django.db import models


class Project(models.Model):
    beginning_date = models.DateField(null=False, blank=False)
    ending_date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)

    def __str__(self):
        return f'project:{self.pk} - {self.name[:40]}'

    class Meta:
        db_table = "project"
        verbose_name = "проект"