from core.models import DockerContainer, DockerImage, User
from django.contrib import admin


class DockerContainerAdmin(admin.ModelAdmin):
    list_display = ("container_name", "image", "allocated_to", "assigned_port", "created_time", "is_killed", "killed_at")

    def is_killed(self, obj):
        return obj.killed_at is not None

    is_killed.short_description = 'Is Killed'
    is_killed.boolean = True

class DockerImageAdmin(admin.ModelAdmin):
  list_display = ("name", "tag", "is_enabled", "port_to_expose", "allocated_port_start", "allocated_port_end", "lifespan", "created_time", "flag")

class UserAdmin(admin.ModelAdmin):
  list_display = ("name", "magic_key", "created_time", "is_active")

admin.site.register(DockerImage, DockerImageAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(DockerContainer, DockerContainerAdmin)
