from django.contrib import admin

from core.models import DockerContainer, DockerImage, User

admin.site.register(DockerImage)
admin.site.register(User)
admin.site.register(DockerContainer)
