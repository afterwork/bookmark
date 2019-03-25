from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.views.generic import TemplateView
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import NotTelegramDataError, TelegramDataIsOutdatedError
from django_telegram_login.widgets.constants import LARGE
from django_telegram_login.widgets.generator import create_redirect_login_widget
from rest_framework import viewsets

from apps.common.views import CustomViewSetMixin
from . import serializers


class TelegramLoginView(TemplateView):
    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["telegram_login_widget"] = create_redirect_login_widget(
            settings.TELEGRAM_LOGIN_REDIRECT_URL, settings.TELEGRAM_BOT_NAME, size=LARGE
        )
        return context


class RegisterUser(TemplateView):
    template_name = "users/login_data.html"

    def check_data(self, **kwargs):
        context = super().get_context_data()
        if not self.request.GET.get("hash"):
            context["error"] = True
            context["message"] = "Handle the missing Telegram data in the response."
            return context
        try:
            result = verify_telegram_authentication(
                bot_token=settings.TELEGRAM_BOT_TOKEN, request_data=self.request.GET
            )
        except TelegramDataIsOutdatedError:
            context["error"] = True
            context["message"] = "Authentication was received more than a day ago."
            return context

        except NotTelegramDataError:
            context["error"] = True
            context["message"] = "The data is not related to Telegram!"
            return context

        user_model = get_user_model()

        try:
            user = user_model.objects.get(username=result["id"])
        except user_model.DoesNotExist:
            user = user_model.objects.create_user(
                username=result.get("id"), first_name=result.get("first_name"), last_name=result.get("last_name")
            )
        login(request=self.request, user=user)
        return context

    def get_context_data(self, **kwargs):
        context = self.check_data(**kwargs)
        return context


class UserViewSet(CustomViewSetMixin, viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = serializers.UserDetailSerializer
