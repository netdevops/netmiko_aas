"""netmiko_aas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from ssh_api import views as ssh_views
from rest_framework import routers
from rest_framework.authtoken import views as auth_views
from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter()
router.register(r'netmiko', ssh_views.SshViewSet, basename="netmiko")

swagger_view = get_swagger_view(title="Netmiko as a Service")

urlpatterns = [
    path('', swagger_view),
    path('api/v1/', include(router.urls)),
    path('api/auth/', auth_views.obtain_auth_token),
    path('admin/', admin.site.urls),
]
