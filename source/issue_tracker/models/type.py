from django.db import models

class Type(models.Model):
    type_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f'type:{self.pk} - {self.type_name}'

    class Meta:
        db_table = "type"
        verbose_name = "тип"