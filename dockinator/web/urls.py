from django.urls import path
from web.views import HomePageView, DeployPageView, KillPageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('public/<str:magic_link>/deploy/', DeployPageView.as_view(), name='deploy'),
    path('public/<str:magic_link>/stop/<str:container_id>',
        KillPageView.as_view(), name='kill'),
]
