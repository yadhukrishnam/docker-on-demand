import uuid

from core.utils import get_container_logs, kill_container, remove_container
from django.db import models
from django.utils import timezone


class DockerImage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tag = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=True)
    port_to_expose = models.IntegerField(default=80)
    allocated_port_start = models.IntegerField(default=0)
    allocated_port_end = models.IntegerField(default=0)
    lifespan = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_time"]

    def __str__(self):
        return f"{self.name} {self.tag}"


class User(models.Model):
    name = models.CharField(max_length=100)
    magic_key = models.UUIDField(default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]


class DockerContainer(models.Model):
    container_id = models.CharField(max_length=100)
    container_name = models.CharField(max_length=2048)
    image = models.ForeignKey(DockerImage, on_delete=models.CASCADE)
    allocated_to = models.ForeignKey("User", on_delete=models.CASCADE)
    assigned_port = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    killed_at = models.DateTimeField(null=True)
    logs = models.TextField(null=True)

    class Meta:
        ordering = ["created_time"]

    def kill(self, auto_remove_container=True):
        kill_container(self.container_id)
        self.killed_at = timezone.now()
        self.logs = get_container_logs(self.container_id)
        if auto_remove_container:
            remove_container(self.container_id)
        self.save()
