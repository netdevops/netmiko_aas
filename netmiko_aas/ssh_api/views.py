from rest_framework import viewsets
from rest_framework import mixins
from .models import Ssh
from .serializers import SshSerializer
from .tasks import netmiko_execution


class SshViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Ssh.objects.all()
    serializer_class = SshSerializer

    def create(self, request, *args, **kwargs):
        execution = super().create(request, *args, **kwargs)
        netmiko_execution.delay(execution.data)
        return execution
