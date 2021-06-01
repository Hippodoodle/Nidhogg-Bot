from django.db import models


class FlaggedWarning(models.Model):
    message_id = models.IntegerField(unique=True)
    red_votes = models.IntegerField(default=0)
    green_votes = models.IntegerField(default=0)
    message_content = models.CharField(max_length=2000, default='')

    def __str__(self) -> str:
        return str(self.message_id)
