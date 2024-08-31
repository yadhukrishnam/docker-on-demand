import requests
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from core.models import DockerContainer, DockerImage, User
from core.utils import generate_pow, validate_pow
from dockinator.settings import PUBLIC_URL
from web.forms import DeployContainerForm


class HomePageView(TemplateView):
    template_name = "home.html"


class DeployPageView(TemplateView):
    template_name = "deploy.html"

    def get(self, request, *args, **kwargs):
        magic_key = kwargs["magic_link"]
        user = get_object_or_404(User, magic_key=magic_key, is_active=True)
        containers = DockerContainer.objects.filter(
            killed_at=None, allocated_to_id=user
        )
        running_image_ids = [container.image.id for container in containers]
        available_images = DockerImage.objects.filter(is_enabled=True)

        if not request.session.get("partial_string"):
            partial_string, required_result, pow_strength = generate_pow()
            request.session.update(
                {
                    "partial_string": partial_string,
                    "required_result": required_result,
                    "pow_strength": pow_strength,
                    "magic_link": magic_key,
                }
            )
        else:
            partial_string = request.session["partial_string"]
            required_result = request.session["required_result"]
            pow_strength = request.session["pow_strength"]

        form = DeployContainerForm(running_image_ids=running_image_ids)

        context = {
            "user": user,
            "form": form,
            "images": available_images,
            "magic_key": magic_key,
            "containers": containers,
            "public_url": PUBLIC_URL,
            "partial_string": partial_string,
            "required_result": required_result,
            "required_chars": f" + {pow_strength} chars",
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        magic_key = kwargs["magic_link"]
        user = get_object_or_404(User, magic_key=magic_key, is_active=True)
        containers = DockerContainer.objects.filter(
            killed_at=None, allocated_to_id=user
        )
        running_image_ids = [container.image.id for container in containers]

        partial_string = request.session["partial_string"]
        required_result = request.session["required_result"]
        pow_strength = request.session["pow_strength"]

        form = DeployContainerForm(
            request.POST,
            running_image_ids=running_image_ids,
            required_result=required_result,
        )

        if form.is_valid():
            image_id = form.cleaned_data["image"].id
            if image_id in running_image_ids:
                context = {
                    "user": user,
                    "form": form,
                    "containers": containers,
                    "public_url": PUBLIC_URL,
                    "partial_string": partial_string,
                    "required_result": required_result,
                    "required_chars": f" + {pow_strength} chars",
                    "error": "Image already running.",
                }
                return render(request, self.template_name, context)

            r = requests.post(
                "http://localhost:8000/api/images/deploy/",
                json={"allocated_to": user.id, "image": image_id},
            )
            print(r.text)
            if r.status_code == 201:
                return redirect(f"/public/{magic_key}/deploy/?success")
            else:
                return redirect(f"/public/{magic_key}/deploy/?error")
        else:
            return redirect(f"/public/{magic_key}/deploy/?wrong_pow")


class KillPageView(TemplateView):
    template_name = "deploy.html"

    def get(self, request, *args, **kwargs):
        magic_key = kwargs["magic_link"]
        user = get_object_or_404(User, magic_key=magic_key, is_active=True)
        container = get_object_or_404(
            DockerContainer,
            container_id=kwargs["container_id"],
            allocated_to_id=user,
            killed_at=None,
        )

        r = requests.delete(
            f"http://localhost:8000/api/container/{container.container_id}/"
        )
        if r.status_code == 200:
            return redirect(f"/public/{magic_key}/deploy/?kill_success")
        else:
            return redirect(f"/public/{magic_key}/deploy/?kill_error")
