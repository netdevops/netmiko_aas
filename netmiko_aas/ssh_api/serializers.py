from rest_framework import serializers
from .models import SshJob


class SshSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SshJob
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
