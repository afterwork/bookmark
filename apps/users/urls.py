from django.conf.urls import include
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView, TokenVerifyView
from . import views

router = SimpleRouter(trailing_slash=False)
router.register("users", viewset=views.UserViewSet)

urlpatterns = [
    path("logout", views.Logout.as_view(), name="logout"),
    path("token/refresh", TokenRefreshSlidingView.as_view(), name="token_refresh"),
    path("login/telegram", views.TelegramLoginView.as_view(), name="telegram_login"),
    path("login/telegram/redirect", views.RegisterUser.as_view(), name="telegram_login_redirect"),
] + router.urls
