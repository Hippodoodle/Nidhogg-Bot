from django.db import models

# Create your models here.

class FlaggedWarning(models.Model):
    message_id = models.IntegerField(unique=True)
    red_votes = models.IntegerField(default=0)
    green_votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.message_id
