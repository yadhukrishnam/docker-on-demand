from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from core.models import DockerContainer, DockerImage, User
from core.serializers import (DockerContainerSerializer, DockerImageSerializer,
                              UserSerializer)


@csrf_exempt
def docker_images_list(request):
    """
    List all docker images, or create a new docker image.
    """
    if request.method == "GET":
        docker_images = DockerImage.objects.all()
        serializer = DockerImageSerializer(docker_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = DockerImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def docker_image_detail(request, pk):
    """
    Retrieve, update or delete a docker image.
    """
    try:
        docker_image = DockerImage.objects.get(pk=pk)
    except DockerImage.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = DockerImageSerializer(docker_image)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = DockerImageSerializer(docker_image, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        docker_image.delete()
        return HttpResponse(status=204)


@csrf_exempt
def deploy_container(request):
    """
    Deploy a container from allowed images.
    """
    if request.method == "POST":
        data = JSONParser().parse(request)
        requested_image = DockerImage.objects.get(name=data["image"])
        data["image"] = requested_image.pk

        requested_for = data.get("allocated_to")
        user = User.objects.filter(name=requested_for).first()
        if user:
            data["allocated_to"] = user.pk
        else:
            raise ("User does not exist.")

        serializer = DockerContainerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return HttpResponse(status=405)


@csrf_exempt
def docker_container_detail(request, container_id):
    """
    Retrieve or kill a docker container.
    """
    try:
        docker_container = DockerContainer.objects.get(container_id=container_id)
    except DockerContainer.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = DockerContainerSerializer(docker_container)
        return JsonResponse(serializer.data)

    elif request.method == "DELETE":
        serializer = DockerContainerSerializer(docker_container)
        try:
            serializer.kill_container(docker_container)
            return HttpResponse(status=204)
        except serializer.ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def get_active_deployments(request):
    """
    Get all active deployed containers of a user
    """
    if request.method == "POST":
        user = User.objects.filter(
            name=JSONParser().parse(request)["name"]
        ).first()
        if user:
            active_containers = DockerContainer.objects.filter(allocated_to=user, killed_at=None)
            serializer = DockerContainerSerializer(active_containers, many=True)
            return JsonResponse({"active_containers": serializer.data})
        return JsonResponse({"error": "User not found."}, status=404)
    return HttpResponse(status=405)

@csrf_exempt
def kill_container(request):
    """
    Kill a container based on image name and user name
    """
    if request.method == "POST":
        data = JSONParser().parse(request)
        user = User.objects.filter(name=data["user"]).first()
        if not user:
            return JsonResponse({"error": "User not found."}, status=404)

        image = DockerImage.objects.filter(name=data["image"]).first()
        if not image:
            return JsonResponse({"error": "Image not found."}, status=404)

        container = DockerContainer.objects.filter(
            image=image.pk, allocated_to=user, killed_at=None
        ).first()
        
        if not container:
            return JsonResponse({"error": "The image has no active deployments."}, status=404)
                        
        serializer = DockerContainerSerializer(container)
        try:
            serializer.kill_container(container)
            return HttpResponse(status=204)
        except serializer.ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponse(status=405)

@csrf_exempt
def get_or_create_user(request):
    """
    Create a new user or return existing user if user already exists
    """
    if request.method == "POST":
        user = User.objects.filter(
            name=JSONParser().parse(request)["name"]
        ).first()
        if user:
            serializer = UserSerializer(user)
            return JsonResponse({"user": serializer.data})

        serializer = UserSerializer(data=JSONParser().parse(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return HttpResponse(status=405)


@csrf_exempt
def user_detail(request, magic_key):
    """
    Get user details and deployed containers for a user 
    """
    try:
        user = User.objects.get(magic_key=magic_key)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = UserSerializer(user)
        deployed_containers = DockerContainer.objects.filter(allocated_to=user)
        deployed_containers_serializer = DockerContainerSerializer(
            deployed_containers, many=True
        )
        return JsonResponse(
            {
                "user": serializer.data,
                "deployed_containers": deployed_containers_serializer.data,
            }
        )
    return HttpResponse(status=405)
