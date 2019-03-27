from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from .models import Bookmark

# Create your views here.


class DashHome(View):
    template_name = "dashboard/home.html"
    context = dict()

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse("telegram_login"))
        else:
            book = Bookmark.objects.all()
            self.context["book"] = book
            self.context["first_name"] = user.first_name
            self.context["last_name"] = user.last_name
            self.context["photo_url"] = user.photo_url

        return render(request, "dashboard/home.html", self.context)
