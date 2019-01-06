from rest_framework import serializers
from .models import Ssh


class SshSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        password = serializers.CharField(max_length=128)
        model = Ssh
        fields = ('id', 'created', 'username', 'host', 'device_type', 'execution_type', 'commands', 'output', 'completed')
