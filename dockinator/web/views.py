from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from core.models import DockerContainer, User, DockerImage
from dockinator.settings import PUBLIC_URL
from core.utils import generate_pow

class HomePageView(TemplateView):
    template_name = 'home.html'

class DeployPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        magic_key = kwargs['magic_link']
        user = get_object_or_404(User, magic_key=magic_key, is_active=True)
        images = DockerImage.objects.filter(is_enabled=True)
        containers = DockerContainer.objects.filter(killed_at=None, allocated_to_id=user)
        running_image_ids = [container.image.id for container in containers]

        if request.session.get('partial_string') == None:            
            partial_string, required_result, pow_strength = generate_pow()
            request.session['partial_string'] = partial_string
            request.session['required_result'] = required_result
            request.session['pow_strength'] = pow_strength
        else: 
            partial_string = request.session['partial_string']
            required_result = request.session['required_result']
            pow_strength = request.session['pow_strength']

        required_chars = f" + {pow_strength} chars"
        context = {
            'user': user,
            'images': images,
            'containers': containers,
            'running_image_ids': running_image_ids,
            "public_url": PUBLIC_URL,
            "partial_string": partial_string,
            "required_result": required_result,
            "required_chars": required_chars,
        }

        return render(request, 'deploy.html', context)
