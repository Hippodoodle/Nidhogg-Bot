from django.contrib import admin
from bot.models import FlaggedWarning, ModerationLog, Guild


class GuildAdmin(admin.ModelAdmin):
    list_display = ['guild_id', 'name']


admin.site.register(FlaggedWarning)
admin.site.register(ModerationLog)
admin.site.register(Guild, GuildAdmin)
