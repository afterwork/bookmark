from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.


class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)


class DashHome(View):
    template_name = "dashboard/home.html"
    context = dict()
    context["ra"] = "mmm"

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse("telegram_login"))
        else:
            self.context["first_name"] = user.first_name
            self.context["last_name"] = user.last_name
        return render(request, "dashboard/home.html", self.context)
