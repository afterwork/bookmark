from django.conf.urls import include
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView, TokenVerifyView
from . import views


urlpatterns = [path("", views.DashHome.as_view(), name="home")]
