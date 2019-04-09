from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.views.generic import TemplateView
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import NotTelegramDataError, TelegramDataIsOutdatedError
from django_telegram_login.widgets.constants import LARGE
from django_telegram_login.widgets.generator import create_redirect_login_widget
from telegram import Bot
from rest_framework import viewsets
from django.shortcuts import redirect
from apps.common.views import CustomViewSetMixin
from . import serializers
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


class TelegramLoginView(TemplateView):
    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["telegram_login_widget"] = create_redirect_login_widget(
            settings.TELEGRAM_LOGIN_REDIRECT_URL, settings.TELEGRAM_BOT_NAME, size=LARGE
        )
        return context


class TelegramUserPhoto:
    photo_url = "https://www.lagersmit.com/wp-content/uploads/2014/09/default_avatar-2.gif"

    def get_photo_url(self, user_id):
        bot = Bot(settings.TELEGRAM_BOT_TOKEN)
        result = bot.getUserProfilePhotos(user_id)
        if result["total_count"] > 0:
            photos = [i.get_file().file_path for i in result.photos[0]]
            self.photo_url = photos[0]


class RegisterUser(TelegramUserPhoto, View):
    template_name = "users/login_data.html"
    context = dict()
    result = dict()
    redirect_url = reverse_lazy("home")

    def set_redirect_url(self, url):
        self.redirect_url = redirect(url)

    def set_error(self, message):
        self.context["error"] = True
        self.context["error_message"] = message

    def check_data(self, request, **kwargs):

        if not self.request.GET.get("hash"):
            self.set_error("Handle the missing Telegram data in the response.")
        else:
            try:
                self.result = verify_telegram_authentication(
                    bot_token=settings.TELEGRAM_BOT_TOKEN, request_data=self.request.GET
                )
            except TelegramDataIsOutdatedError:
                self.set_error("Authentication was received more than a day ago.")

            except NotTelegramDataError:
                self.set_error("The data is not related to Telegram!")

        if "error" in self.context and self.context["error"]:
            return render(request, self.template_name, self.context)

        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=self.result["id"])
        except user_model.DoesNotExist:
            if self.result.get("photo_url"):
                self.photo_url = self.result.get("photo_url")
            else:
                self.get_photo_url(self.result.get("id"))
            user = user_model.objects.create_user(
                username=self.result.get("id"),
                first_name=self.result.get("first_name"),
                last_name=self.result.get("last_name"),
                photo_url=self.photo_url,
            )

        login(request=self.request, user=user)
        self.set_redirect_url(reverse("home"))
        return self.redirect_url

    def get(self, request, **kwargs):
        response = self.check_data(request, **kwargs)
        return response


class Logout(LogoutView):
    logout_then_login = reverse_lazy("telegram_login")


class UserViewSet(CustomViewSetMixin, viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = serializers.UserDetailSerializer
