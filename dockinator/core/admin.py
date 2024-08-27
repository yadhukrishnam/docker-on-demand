from django.contrib import admin
from core.models import DockerImage, User, DockerContainer

admin.site.register(DockerImage)
admin.site.register(User)
admin.site.register(DockerContainer)
