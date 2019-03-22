from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, permissions, generics, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.conf import settings
from django.views.generic import TemplateView
from apps.common.views import CustomViewSetMixin, CustomSerializerViewSetMixin
from . import serializers, models

from django_telegram_login.widgets.constants import SMALL, MEDIUM, LARGE, DISABLE_USER_PHOTO
from django_telegram_login.widgets.generator import create_callback_login_widget, create_redirect_login_widget


class TelegramLoginView(TemplateView):

    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        bot_name = settings.TELEGRAM_BOT_NAME
        bot_token = settings.TELEGRAM_BOT_TOKEN
        redirect_url = settings.TELEGRAM_LOGIN_REDIRECT_URL
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context["telegram_login_widget"] = create_callback_login_widget(bot_name, size=SMALL)
        return context


class UserViewSet(CustomViewSetMixin, viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = serializers.UserDetailSerializer
