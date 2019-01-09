from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import SshJob
from .serializers import SshSerializer
from .tasks import netmiko_execution


class SshViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = SshJob.objects.all()
    serializer_class = SshSerializer
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        source = request.META.get("REMOTE_ADDR", None)
        credentials = request.META.get("HTTP_NETAUTH", None)
        request = super().create(request, *args, **kwargs)
        request.data["source"] = source
        request.data["username"] = credentials.split(":")[0]
        request.data["password"] = credentials.split(":")[1]
        netmiko_execution.delay(request.data)
        request.data.pop("password", None)
        return request
