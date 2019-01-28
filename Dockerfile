FROM python:3.6-stretch

WORKDIR /opt

COPY . netmiko_aas
COPY supervisord.conf /etc/supervisord.conf

ENV NETMIKO_AAS_SECRET_KEY="6nHN0YSF$IzETS^Uiw^Iaq#ZX5ZJIGOpVZ*GEYbl4Yo2#7aeula^l7v%pbl"
ENV NETMIKO_AAS_DEBUG=False
ENV NETMIKO_AAS_DB_NAME="naasdb"
ENV NETMIKO_AAS_DB_USER="postgres"
ENV NETMIKO_AAS_DB_PASS="mysecretpassword"
ENV NETMIKO_AAS_DB_HOST="postgres"
ENV NETMIKO_AAS_DB_PORT=5432
ENV NETMIKO_AAS_BROKER_URL="redis://redis:6379"
ENV NETMIKO_AAS_CELERY_RESULT_BACKEND="redis://redis:6379"

EXPOSE 8000

RUN pip install -r ./netmiko_aas/requirements.txt
RUN pip install git+https://github.com/Supervisor/supervisor

CMD ["supervisord"]
