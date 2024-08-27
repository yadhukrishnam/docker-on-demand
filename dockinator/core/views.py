from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from core.models import DockerImage, DockerContainer, User
from core.serializers import DockerImageSerializer, UserSerializer, DockerContainerSerializer


@csrf_exempt
def docker_images_list(request):
    """
    List all docker images, or create a new docker image.
    """
    if request.method == 'GET':
        docker_images = DockerImage.objects.all()
        serializer = DockerImageSerializer(docker_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
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

    if request.method == 'GET':
        serializer = DockerImageSerializer(docker_image)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DockerImageSerializer(docker_image, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        docker_image.delete()
        return HttpResponse(status=204)


@csrf_exempt
def deploy_docker_image(request):
    """
    Deploy a docker image.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
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
        docker_container = DockerContainer.objects.get(
            container_id=container_id)
    except DockerContainer.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DockerContainerSerializer(docker_container)
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        serializer = DockerContainerSerializer(docker_container)
        try:
            serializer.kill_container(docker_container)
            return HttpResponse(status=204)
        except serializer.ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def create_user(request):
    """
    Create a new user
    """
    if request.method == 'POST':
        user_exists = User.objects.filter(
            name=JSONParser().parse(request)['name']).exists()
        if user_exists:
            return JsonResponse({'error': 'User already exists.'}, status=400)

        serializer = UserSerializer(data=JSONParser().parse(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return HttpResponse(status=405)


@csrf_exempt
def user_detail(request, name):
    """
    Get user details and deployed containers for a user
    """
    try:
        user = User.objects.get(name=name)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        deployed_containers = DockerContainer.objects.filter(allocated_to=user)
        deployed_containers_serializer = DockerContainerSerializer(
            deployed_containers, many=True)
        return JsonResponse({'user': serializer.data, 'deployed_containers': deployed_containers_serializer.data})
    return HttpResponse(status=405)
