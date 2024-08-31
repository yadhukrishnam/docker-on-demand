import uuid

from django.utils import timezone
from docker.errors import APIError
from rest_framework import serializers

from core.models import DockerContainer, DockerImage, User
from core.utils import deploy_container, is_image_available, kill_container


class DockerImageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    tag = serializers.CharField(max_length=100)
    is_enabled = serializers.BooleanField(default=False, required=False)
    port_to_expose = serializers.IntegerField(required=True)
    allocated_port_start = serializers.IntegerField(required=True)
    allocated_port_end = serializers.IntegerField(required=True)
    lifespan = serializers.IntegerField(default=0)
    created_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DockerImage
        fields = [
            "id",
            "name",
            "tag",
            "is_enabled",
            "port_to_expose",
            "allocated_port_start",
            "allocated_port_end",
            "lifespan",
            "created_time",
        ]

    def create(self, validated_data):
        if not is_image_available(
            validated_data.get("name"), validated_data.get("tag")
        ):
            raise serializers.ValidationError(
                "Image does not exist in the local registry."
            )

        return DockerImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.tag = validated_data.get("tag", instance.tag)
        instance.is_enabled = validated_data.get("is_enabled", instance.is_enabled)
        instance.port_to_expose = validated_data.get(
            "port_to_expose", instance.port_to_expose
        )
        instance.allocated_port_start = validated_data.get(
            "allocated_port_start", instance.allocated_port_start
        )
        instance.allocated_port_end = validated_data.get(
            "allocated_port_end", instance.allocated_port_end
        )
        instance.lifespan = validated_data.get("lifespan", instance.lifespan)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    magic_key = serializers.UUIDField(default=uuid.uuid4, read_only=True)
    created_time = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = ["id", "name", "magic_key", "created_time", "is_active"]

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class DockerContainerSerializer(serializers.ModelSerializer):
    container_id = serializers.CharField(max_length=100, read_only=True)
    container_name = serializers.CharField(max_length=2048, read_only=True)
    image = serializers.PrimaryKeyRelatedField(queryset=DockerImage.objects.all())
    allocated_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    assigned_port = serializers.IntegerField(read_only=True)
    created_time = serializers.DateTimeField(read_only=True)
    killed_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DockerContainer
        fields = [
            "id",
            "container_id",
            "container_name",
            "image",
            "allocated_to",
            "assigned_port",
            "created_time",
            "killed_at",
        ]

    def create(self, validated_data):
        image = validated_data.get("image")

        user = validated_data.get("allocated_to")

        if not image.is_enabled:
            raise serializers.ValidationError("Image is not enabled.")

        if not user.is_active:
            raise serializers.ValidationError("User is not active.")

        port_range = range(image.allocated_port_start, image.allocated_port_end + 1)
        assigned_port = next(
            (
                port
                for port in port_range
                if not DockerContainer.objects.filter(
                    assigned_port=port, killed_at=None
                ).exists()
            ),
            None,
        )
        container_name = f"{image.name}-{user.name}-{assigned_port}"
        container_id = deploy_container(
            f"{image.name}:{image.tag}",
            container_name,
            image.port_to_expose,
            assigned_port,
        )

        if assigned_port is None:
            raise serializers.ValidationError(
                "No available ports in the specified range."
            )

        print(
            "Assigned port: ",
            assigned_port,
            " for internal container_id: ",
            container_id,
            "for user",
            user.name,
        )
        return DockerContainer.objects.create(
            assigned_port=assigned_port,
            container_name=container_name,
            container_id=container_id,
            **validated_data,
        )

    def kill_container(self, instance):
        try:
            container = DockerContainer.objects.get(pk=instance.pk)
            print("Killing container: ", container.container_id)
            logs = kill_container(container.container_id)
            container.killed_at = timezone.now()
            container.logs = logs
            container.save()
        except APIError:
            raise serializers.ValidationError("Container could not be killed.")
