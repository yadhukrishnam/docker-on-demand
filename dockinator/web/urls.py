from django.urls import path
from web.views import HomePageView, DeployPageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('public/<str:magic_link>/', DeployPageView.as_view(), name='deploy'),
]