from core import views
from django.urls import path

urlpatterns = [
    path ("user/get_or_create", views.get_or_create_user),
    path ("user/get_active_deployments", views.get_active_deployments),
    path ("user/container/kill", views.kill_container),
    path ("container/deploy", views.deploy_container),

    # path("images/", views.docker_images_list),
    # path("images/<int:pk>/", views.docker_image_detail),
    # path("images/deploy/", views.deploy_docker_image),
    # 
    # path("container/<str:container_id>/", views.docker_container_detail),
    # path("users/create", views.create_user),
    # path("users/<str:magic_key>/", views.user_detail),
]
