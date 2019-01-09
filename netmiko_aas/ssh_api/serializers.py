from rest_framework import serializers
from .models import Ssh


class SshSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ssh
        fields = ('id', 'created', 'username', 'source', 'host', 'device_type', 'execution_type', 'commands', 'output', 'completed')
