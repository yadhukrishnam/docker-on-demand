from django.core.management.base import BaseCommand
import docker.errors
from core.models import DockerContainer
from datetime import timedelta
from django.utils import timezone
import docker


def get_expired_containers():
    expired = []
    for container in DockerContainer.objects.filter(killed_at=None):
        if (
            container.created_time + timedelta(seconds=container.image.lifespan)
            < timezone.now()
        ):
            expired.append(container)
    return expired


class Command(BaseCommand):
    help = "Manage expired docker containers"

    def add_arguments(self, parser):
        parser.add_argument(
            "-l",
            "--list-only",
            action="store_true",
            help="List docker containers that have expired.",
        )
        parser.add_argument(
            "-k",
            "--kill-expired",
            action="store_true",
            help="Kill all expired docker containers.",
        )

    def handle(self, *args, **kwargs):
        list_only = kwargs["list_only"]
        kill_expired = kwargs["kill_expired"]
        expired_containers = get_expired_containers()

        if list_only:
            for container in expired_containers:
                self.stdout.write(
                    f"Container Name: {container.container_id}, ID: {container.id}"
                )

        if kill_expired:
            for container in expired_containers:
                try:
                    container.kill()
                    self.stdout.write(f"Container {container.container_id} killed.")
                except docker.errors.NotFound:
                    self.stdout.write(f"Container {container.container_id} not found.")
                    continue
