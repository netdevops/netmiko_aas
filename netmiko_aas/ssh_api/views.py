from rest_framework import viewsets
from rest_framework import mixins
from .models import Ssh
from .serializers import SshSerializer
from .tasks import netmiko_execution
import simplejson as json


class SshViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Ssh.objects.all()
    serializer_class = SshSerializer

    def create(self, request, *args, **kwargs):
        source = request.META.get("REMOTE_ADDR", None)
        credentials = json.loads(request.META.get("HTTP_NETAUTH", None))
        request = super().create(request, *args, **kwargs)
        request.data["source"] = source
        request.data["username"] = credentials.get("username", None)
        request.data["password"] = credentials.get("password", None)
        netmiko_execution.delay(request.data)
        request.data.pop("password", None)
        return request
