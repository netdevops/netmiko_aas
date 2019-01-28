# Netmiko as a Service

At the moment this is just a POC.

## Developement Environment

* Spin up a development Postgres docker instance
```
docker run -d --name naasdb -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=naasdb -p 5432:5432 postgres
```
* Spin up a development Redis docker instance
```
docker run -d --name naascache -p 6379:6379 redis
```
* Setup Python virtual environment
```
cd netmiko_aas
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
* Setup database tables
```
./manage.py migrate
```
* Spin up Celery
```
celery -A netmiko_aas worker -l INFO
```
* Create Admin User
```
./manage.py createsuperuser
```
* Run development server
```
./manage.py runserver
```

## Curl Operations

## Create Authentication Token
To obtain an authentication token, the user associated with the token must exist as a user in django.
```
curl -X POST "http://localhost:8000/auth/" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"jtdub\", \"password\": \"somepassword\"}"

{"token": "70fe753a3e602f0da51ef05a9f3c59d7c52e9649"}
```

To create new tasks, you have to send a POST operation with `"NETAUTH: <username>:<password>"` in the headers.
These credentials are used to log into the remote machine.

### POST
```
curl -X POST "http://localhost:8000/netmiko/" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"host\": \"watch\", \"device_type\": \"linux\", \"execution_type\": \"execution\", \"commands\": [ \"ping -c 2 1.1.1.1\" ]}" -H "NETAUTH: <tacacs_user>:<tacacs_password>" -H "Authorization: Token 70fe753a3e602f0da51ef05a9f3c59d7c52e9649"

{"id":1,"created":"2019-01-09T01:28:53.755381Z","username":"jtdub","source":"127.0.0.1","host":"watch","device_type":"linux","execution_type":"execution","commands":["ping -c 2 1.1.1.1"],"output":"","completed":null}
```



### GET (single post)
```
curl -X GET http://localhost:8000/netmiko/1/ -H "Authorization: Token 70fe753a3e602f0da51ef05a9f3c59d7c52e9649"

{"id":1,"created":"2019-01-09T01:28:53.755381Z","username":"jtdub","source":"127.0.0.1","host":"watch","device_type":"linux","execution_type":"execution","commands":["ping -c 2 1.1.1.1"],"output":"PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.\n64 bytes from 1.1.1.1: icmp_seq=1 ttl=54 time=19.8 ms\n64 bytes from 1.1.1.1: icmp_seq=2 ttl=54 time=18.6 ms\n\n--- 1.1.1.1 ping statistics ---\n2 packets transmitted, 2 received, 0% packet loss, time 1001ms\nrtt min/avg/max/mdev = 18.688/19.276/19.865/0.604 ms","completed":"2019-01-09T01:28:59.776658Z"}
```

### GET (pagination posts)
```
curl -X GET http://localhost:8000/netmiko/ -H "Authorization: Token 70fe753a3e602f0da51ef05a9f3c59d7c52e9649"

{"count":20,"next":"http://localhost:8000/netmiko/?page=2","previous":null,"results":[{"id":1,"created":"2019-01-09T01:28:53.755381Z","username":"jtdub","source":"127.0.0.1","host":"watch","device_type":"linux","execution_type":"execution","commands":["ping -c 2 1.1.1.1"],"output":"PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.\n64 bytes from 1.1.1.1: icmp_seq=1 ttl=54 time=19.8 ms\n64 bytes from 1.1.1.1: icmp_seq=2 ttl=54 time=18.6 ms\n\n--- 1.1.1.1 ping statistics ---\n2 packets transmitted, 2 received, 0% packet loss, time 1001ms\nrtt min/avg/max/mdev = 18.688/19.276/19.865/0.604 ms","completed":"2019-01-09T01:28:59.776658Z"},{"id":2,"created":"2019-01-09T01:29:48.652945Z","username":"jtdub","source":"127.0.0.1","host":"watch","device_type":"linux","execution_type":"execution","commands":["ping -c 2 1.1.1.1"],"output":"PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.\n64 bytes from 1.1.1.1: icmp_seq=1 ttl=54 time=23.0 ms\n64 bytes from 1.1.1.1: icmp_seq=2 ttl=54 time=27.9 ms\n\n--- 1.1.1.1 ping statistics ---\n2 packets transmitted, 2 received, 0% packet loss, time 1000ms\nrtt min/avg/max/mdev = 23.046/25.477/27.908/2.431 ms","completed":"2019-01-09T01:29:54.655860Z"},{"id":3,"created":"2019-01-09T01:29:49.944640Z","username":"jtdub","source":"127.0.0.1","host":"watch","device_type":"linux","execution_type":"execution","commands":["ping -c 2 1.1.1.1"],"output":"PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.\n64 bytes from 1.1.1.1: icmp_seq=1 ttl=54 time=19.3 ms\n64 bytes from 1.1.1.1: icmp_seq=2 ttl=54 time=22.4 ms\n\n--- 1.1.1.1 ping statistics ---\n2 packets transmitted, 2 received, 0% packet loss, time 1001ms\nrtt min/avg/max/mdev = 19.343/20.872/22.401/1.529 ms","completed":"2019-01-09T01:29:55.700811Z"},{"id":4,"created":"2019-01-09T01:29:50.746253Z","username":"jtdub","source":"127.0.0.1","host":"watch","device_type":"linux","execution_type":"execution","commands":["ping -c 2 1.1.1.1"],"output":"PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.\n64 bytes from 1.1.1.1: icmp_seq=1 ttl=54 time=23.6 ms\n64 bytes from 1.1.1.1: icmp_seq=2 ttl=54 time=21.2 ms\n\n--- 1.1.1.1 ping statistics ---\n2 packets transmitted, 2 received, 0% packet loss, time 1001ms\nrtt min/avg/max/mdev = 21.226/22.423/23.621/1.206 ms","completed":"2019-01-09T01:29:56.708170Z"},{"id":5,"created":"2019-01-09T01:29:51.478123Z","username":"jtdub","source":"127.0.0.1","host":"watch","device_type":"linux","execution_type":"execution","commands":["ping -c 2 1.1.1.1"],"output":"PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.\n64 bytes from 1.1.1.1: icmp_seq=1 ttl=54 time=20.8 ms\n64 bytes from 1.1.1.1: icmp_seq=2 ttl=54 time=24.5 ms\n\n--- 1.1.1.1 ping statistics ---\n2 packets transmitted, 2 received, 0% packet loss, time 1000ms\nrtt min/avg/max/mdev = 20.812/22.703/24.594/1.891 ms","completed":"2019-01-09T01:29:57.321706Z"},{"id":6,"created":"2019-01-09T01:29:52.052213Z","username":"jtdub","source":"127.0.0.1","host":"watch","device_type":"linux","execution_type":"execution","commands":["ping -c 2 1.1.1.1"],"output":"PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.\n64 bytes from 1.1.1.1: icmp_seq=1 ttl=54 time=19.1 ms\n64 bytes from 1.1.1.1: icmp_seq=2 ttl=54 time=22.2 ms\n\n--- 1.1.1.1 ping statistics ---\n2 packets transmitted, 2 received, 0% packet loss, time 1001ms\nrtt min/avg/max/mdev = 19.130/20.667/22.205/1.544 ms","completed":"2019-01-09T01:30:00.443928Z"},{"id":7,"created":"2019-01-09T01:29:52.629188Z","username":"jtdub","source":"127.0.0.1","host":"watch","device_type":"linux","execution_type":"execution","commands":["ping -c 2 1.1.1.1"],"output":"PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.\n64 bytes from 1.1.1.1: icmp_seq=1 ttl=54 time=24.7 ms\n64 bytes from 1.1.1.1: icmp_seq=2 ttl=54 time=16.8 ms\n\n--- 1.1.1.1 ping statistics ---\n2 packets transmitted, 2 received, 0% packet loss, time 1001ms\nrtt min/avg/max/mdev = 16.899/20.822/24.745/3.923 ms","completed":"2019-01-09T01:30:01.473942Z"},{"id":8,"created":"2019-01-09T01:29:53.128810Z","username":"jtdub","source":"127.0.0.1","host":"watch","device_type":"linux","execution_type":"execution","commands":["ping -c 2 1.1.1.1"],"output":"PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.\n64 bytes from 1.1.1.1: icmp_seq=1 ttl=54 time=23.2 ms\n64 bytes from 1.1.1.1: icmp_seq=2 ttl=54 time=19.0 ms\n\n--- 1.1.1.1 ping statistics ---\n2 packets transmitted, 2 received, 0% packet loss, time 999ms\nrtt min/avg/max/mdev = 19.042/21.121/23.200/2.079 ms","completed":"2019-01-09T01:30:02.648076Z"},{"id":9,"created":"2019-01-09T01:29:53.631442Z","username":"jtdub","source":"127.0.0.1","host":"watch","device_type":"linux","execution_type":"execution","commands":["ping -c 2 1.1.1.1"],"output":"PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.\n64 bytes from 1.1.1.1: icmp_seq=1 ttl=54 time=26.3 ms\n64 bytes from 1.1.1.1: icmp_seq=2 ttl=54 time=24.2 ms\n\n--- 1.1.1.1 ping statistics ---\n2 packets transmitted, 2 received, 0% packet loss, time 1000ms\nrtt min/avg/max/mdev = 24.276/25.292/26.308/1.016 ms","completed":"2019-01-09T01:30:03.260387Z"},{"id":10,"created":"2019-01-09T01:29:54.095993Z","username":"jtdub","source":"127.0.0.1","host":"watch","device_type":"linux","execution_type":"execution","commands":["ping -c 2 1.1.1.1"],"output":"PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.\n64 bytes from 1.1.1.1: icmp_seq=1 ttl=54 time=21.5 ms\n64 bytes from 1.1.1.1: icmp_seq=2 ttl=54 time=24.2 ms\n\n--- 1.1.1.1 ping statistics ---\n2 packets transmitted, 2 received, 0% packet loss, time 1001ms\nrtt min/avg/max/mdev = 21.503/22.897/24.292/1.402 ms","completed":"2019-01-09T01:30:06.335297Z"}]}

```

## Python Client Usage

### Create a Token

```
In [4]: from naas_client import NaasClient
In [5]: token = NaasClient(api_username="jtdub", api_password="asdfasdf", url="http://localhost:8000/")
In [6]: token = token.create_token()
In [7]: token
Out[7]: {'token': '412281028778e53e9bfc3da0bcc409bac1cc1b7d'}
```

### Create a Task
```
In [13]: device = {"net_username": "jtdub",
    ...:           "net_password": "asdfasdf",
    ...:           "device_type": "linux",
    ...:           "host": "172.16.1.1",
    ...:           "commands": ["ip route", "date"],
    ...:           "execution_type": "execution"}
    ...:
    ...:

In [14]: naas = NaasClient(url="http://localhost:8000/", token=token['token'], **device)
In [15]: output = naas.post()
In [16]: output
Out[16]:
{'commands': ['ip route', 'date'],
 'completed': None,
 'created': '2019-01-28T22:40:01.405298Z',
 'device_type': 'linux',
 'execution_type': 'execution',
 'host': '172.16.1.1',
 'id': 1,
 'output': '',
 'source': '172.17.0.1',
 'username': 'jtdub'}
 ```

### Fetch a Tasks Results
```
In [17]: output = naas.get(id=1)
In [18]: output
Out[18]:
{'commands': ['ip route', 'date'],
 'completed': '2019-01-28T22:40:07.077638Z',
 'created': '2019-01-28T22:40:01.405298Z',
 'device_type': 'linux',
 'execution_type': 'execution',
 'host': '172.16.1.1',
 'id': 1,
 'output': 'default via 24.55.0.1 dev eth4  proto zebra \n24.55.0.0/19 dev eth4  proto kernel  scope link  src 24.55.13.3 \n172.16.1.0/24 dev switch0  proto kernel  scope link  src 172.16.1.1 Mon Jan 28 22:40:06 UTC 2019',
 'source': '172.17.0.1',
 'username': 'jtdub'}
 ```

## Example Production Deployment in Docker

In this example, we're using docker for the Postgres and Redis databases as well.

### Deploy Database Containers
```
docker run -d --name naasdb -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=naasdb -p 5432:5432 postgres
docker run -d --name naascache redis
```

### Build the Netmiko As A Service Container
```
docker build -t netmiko_aas:latest .
```

### Install the Database Schema and Create the Initial Admin User
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

export NETMIKO_AAS_DB_NAME="naasdb"
export NETMIKO_AAS_DB_USER="postgres"
export NETMIKO_AAS_DB_PASS="mysecretpassword"
export NETMIKO_AAS_DB_HOST="naasdb"

./manage.py migrate
./manage.py createsuperuser
```

### Spin up the Netmiko As A Service Container
```
docker run -it -p 8000:8000 \
--name naas \
--link naasdb \
--link naascache \
-e NETMIKO_AAS_DB_NAME=$NETMIKO_AAS_DB_NAME \
-e NETMIKO_AAS_DB_USER=$NETMIKO_AAS_DB_USER \
-e NETMIKO_AAS_DB_PASS=$NETMIKO_AAS_DB_PASS \
-e NETMIKO_AAS_DB_HOST=$NETMIKO_AAS_DB_HOST \
-e NETMIKO_AAS_BROKER_URL=redis://naascache:6379 \
-e NETMIKO_AAS_CELERY_RESULT_BACKEND=redis://naascache:6379 \
-e NETMIKO_AAS_SECRET_KEY=6nHN0YSF$IzETS^Uiw^Iaq#ZX5ZJIGOpVZ*GEYbl4Yo2#7aeula^l7v%pbl \
netmiko_aas
```
