FROM python:3.9-slim-buster
WORKDIR /opt/docker-on-demand
RUN mkdir -p /opt/docker-on-demand /var/log/docker-on-demand /var/data

COPY server/ /opt/docker-on-demand/
RUN pip install -r requirements.txt --no-cache-dir


RUN adduser --disabled-login -u 1001 --gecos "" --shell /bin/bash duser && \
    chmod +x /opt/docker-on-demand/docker-entrypoint.sh && \
    chown -R 1001:1001 /opt/docker-on-demand /var/log/docker-on-demand /var/data

USER 1001
EXPOSE 1337
ENTRYPOINT ["/opt/docker-on-demand/docker-entrypoint.sh"]
