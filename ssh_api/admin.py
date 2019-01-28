from django.contrib import admin
from .models import SshJob

# Register your models here.

FIELDS = ('id',
          'created',
          'username',
          'source',
          'host',
          'device_type',
          'execution_type',
          'commands',
          'output',
          'completed')


class SshAdmin(admin.ModelAdmin):
    list_display = FIELDS
    search_fields = FIELDS


admin.site.register(SshJob, SshAdmin)
