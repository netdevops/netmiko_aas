from rest_framework import viewsets
from rest_framework import mixins
from .models import Ssh
from .serializers import SshCreateSerializer
from .serializers import SshFetchSerializer
from .tasks import netmiko_execution


class SshCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Ssh.objects.all()
    serializer_class = SshCreateSerializer

    def create(self, request, *args, **kwargs):
        execution = super().create(request, *args, **kwargs)
        netmiko_execution.delay(execution.data)
        return execution


class SshFetchViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Ssh.objects.all()
    serializer_class = SshFetchSerializer
