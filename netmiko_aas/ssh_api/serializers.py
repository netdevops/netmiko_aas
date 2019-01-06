from rest_framework import serializers
from .models import Ssh


class SshCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ssh
        fields = ('id', 'created', 'username', 'host', 'device_type', 'execution_type', 'commands')


class SshFetchSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ssh
        fields = ('id', 'created', 'username', 'host', 'device_type', 'execution_type', 'commands', 'output', 'completed')
