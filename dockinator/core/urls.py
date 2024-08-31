from django.urls import path

from core import views

urlpatterns = [
    path("images/", views.docker_images_list),
    path("images/<int:pk>/", views.docker_image_detail),
    path("images/deploy/", views.deploy_docker_image),
    path("container/<str:container_id>/", views.docker_container_detail),
    path("users/create", views.create_user),
    path("users/<str:magic_key>/", views.user_detail),
]
