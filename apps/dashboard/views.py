from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from .models import Bookmark
from .forms import BookmarkForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView

# Create your views here.


class BookmarkDeleteView(LoginRequiredMixin, DeleteView):
    model = Bookmark
    context_object_name = "Bookmark"
    success_url = reverse_lazy("home")


class BookmarkFormView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("telegram_login")
    template_name = "dashboard/bookmark_create.html"
    form_class = BookmarkForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DashHome(LoginRequiredMixin, View):
    template_name = "dashboard/home.html"
    context = dict()
    login_url = reverse_lazy("telegram_login")

    def get(self, request):
        user = request.user
        book = Bookmark.objects.all().filter(author=request.user)
        self.context["book"] = book
        self.context["first_name"] = user.first_name
        self.context["last_name"] = user.last_name
        self.context["photo_url"] = user.photo_url

        return render(request, "dashboard/home.html", self.context)
