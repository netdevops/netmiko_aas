from django.contrib import admin
from .models import Ssh

# Register your models here.

fields = ('id',
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
    list_display = fields
    search_fields = fields


admin.site.register(Ssh, SshAdmin)
