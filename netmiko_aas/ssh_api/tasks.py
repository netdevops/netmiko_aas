from celery import shared_task
from ssh_api.models import Ssh
from django.utils import timezone
from netmiko import ConnectHandler
from os import environ


@shared_task
def netmiko_execution(request):
    output = str()
    database = Ssh()
    database.id = request["id"]
    database.refresh_from_db()
    device = {
        "device_type": request["device_type"],
        "host": request["host"],
        "username": request["username"],
        "password": environ.get("NETMIKO_PASSWORD", None),
        "verbose": True,
    }

    with ConnectHandler(**device) as ssh:
        if request["execution_type"] == "execution":
            for command in request["commands"]:
                output += ssh.send_command(command)
        else:
            output += ssh.send_config_set(request["commands"])

    database.output = output
    database.completed = timezone.now()
    database.save()

    return {"id": request["id"], "output": output, "completed": timezone.now()}
