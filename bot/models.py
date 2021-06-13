from django.db import models


class Guild(models.Model):
    guild_id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.guild_id)


class ModerationLog(models.Model):
    channel_id = models.IntegerField(unique=True, primary_key=True)
    guild = models.OneToOneField(Guild, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.channel_id)


class FlaggedWarning(models.Model):
    message_id = models.IntegerField(unique=True, primary_key=True)
    red_votes = models.IntegerField(default=0)
    green_votes = models.IntegerField(default=0)
    message_content = models.CharField(max_length=2000, default='')
    moderation_log_channel_id = models.ForeignKey(ModerationLog, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.message_id)
