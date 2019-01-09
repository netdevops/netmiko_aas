from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import SshJob
from .serializers import SshSerializer
from .tasks import netmiko_execution
import simplejson as json


class SshViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = SshJob.objects.all()
    serializer_class = SshSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        source = request.META.get("REMOTE_ADDR", None)
        credentials = json.loads(request.META.get("HTTP_NETAUTH", None))
        request = super().create(request, *args, **kwargs)
        request.data["source"] = source
        request.data["username"] = credentials.get("username", None)
        request.data["password"] = credentials.get("password", None)
        netmiko_execution.delay(request.data)
        request.data.pop("password", None)
        return request
