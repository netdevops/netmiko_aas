from django.contrib import admin
from django.urls import include, path
from . import views as ssh_views
from rest_framework import routers
from rest_framework.authtoken import views as auth_views
from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter()
router.register(r'netmiko', ssh_views.SshViewSet, basename="netmiko")

swagger_view = get_swagger_view(title="Netmiko as a Service")

urlpatterns = [
    path('docs/', swagger_view),
    path('auth/', auth_views.obtain_auth_token),
    path('accounts/', admin.site.urls),
    path('', include(router.urls))
]
