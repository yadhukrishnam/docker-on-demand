from django.conf import settings
from django.http import JsonResponse


def api_key_required(view_func):
    """
    Decorator to check if the request contains a valid API key in the headers.
    """
    def wrapped_view(request, *args, **kwargs):
        api_token = request.headers.get('X-Api-Token')

        if not api_token or api_token not in getattr(settings, 'API_TOKENS', [settings.API_TOKEN]):
            return JsonResponse({'error': 'Invalid or missing API Token'}, status=403)

        return view_func(request, *args, **kwargs)

    return wrapped_view