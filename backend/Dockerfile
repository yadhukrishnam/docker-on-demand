FROM python:3.9-slim-buster

WORKDIR /opt/docker-on-demand

RUN mkdir -p /opt/docker-on-demand/logs /var/log/docker-on-demand /var/data

EXPOSE 1337

COPY config/ /opt/docker-on-demand/config/

COPY server/ /opt/docker-on-demand/

RUN pip install -r requirements.txt --no-cache-dir

RUN chmod +x /opt/docker-on-demand/docker-entrypoint.sh

ENTRYPOINT ["/opt/docker-on-demand/docker-entrypoint.sh"]
