from core.models import DockerContainer, DockerImage, User
from django.contrib import admin

admin.site.register(DockerImage)
admin.site.register(User)
admin.site.register(DockerContainer)
