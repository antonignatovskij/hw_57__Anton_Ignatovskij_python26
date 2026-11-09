from django.db import models
from issue_tracker.validators import IsItLinkValidator, BanWordValidator

class Type(models.Model):
    type_name = models.CharField(max_length=50, validators=[BanWordValidator(), IsItLinkValidator()], null=False, blank=False)

    def __str__(self):
        return f'{self.type_name}'

    class Meta:
        db_table = "type"
        verbose_name = "тип"