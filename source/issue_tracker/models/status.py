from django.db import models
from issue_tracker.validators import IsItLinkValidator, BanWordValidator

class Status(models.Model):
    status_name = models.CharField(max_length=50, validators=[BanWordValidator(), IsItLinkValidator()], null=False, blank=False)

    def __str__(self):
        return f'{self.status_name}'

    class Meta:
        db_table = "status"
        verbose_name = "статус"