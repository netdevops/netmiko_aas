from django.contrib import admin
from .models import Ssh

# Register your models here.

admin.site.register(Ssh)


class SshAdmin(admin.ModelAdmin):
    list_display = ('id', 'created' 'username', 'host', 'type', 'commands')
    search_fields = ('id', 'created', 'username', 'host', 'device_type', 'execution_type', 'commands', 'completed')
