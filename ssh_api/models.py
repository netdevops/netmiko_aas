from django.contrib.postgres.fields import ArrayField
from django.db import models


EXECUTION_TYPES = [('execution', 'Non-configuration commands'),
                   ('configuration', 'Configuration commands')]


class SshJob(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=64, editable=False)
    source = models.GenericIPAddressField(default="0.0.0.0", editable=False)
    host = models.CharField(default='', blank=False, max_length=256)
    device_type = models.CharField(default='', blank=False, max_length=128)
    execution_type = models.CharField(choices=EXECUTION_TYPES, default='execution', max_length=32)
    commands = ArrayField(models.TextField(blank=False))
    output = models.TextField(blank=True, editable=False)
    completed = models.DateTimeField(null=True, editable=False)

    class Meta:
        ordering = ('created',)
