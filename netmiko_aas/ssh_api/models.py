from django.contrib.postgres.fields import ArrayField
from django.db import models


EXECUTION_TYPES = [('execution', 'Non-configuration commands'),
                   ('configuration', 'Configuration commands')]


class Ssh(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=64)
    host = models.CharField(default='', blank=False, max_length=256)
    device_type = models.CharField(default='', blank=False, max_length=128)
    execution_type = models.CharField(choices=EXECUTION_TYPES, default='execution', max_length=32)
    commands = ArrayField(models.TextField(blank=False))
    output = models.TextField(blank=True)
    completed = models.DateTimeField(null=True)

    class Meta:
        ordering = ('created',)
