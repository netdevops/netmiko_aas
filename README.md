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
* Run development server
```
./manage.py runserver
```
