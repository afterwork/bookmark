from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import BookmarkForm
from .models import Bookmark


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

    def post(self, request, *args, **kwargs):
        a = 42
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BookmarkUpdateView(UpdateView):
    model = Bookmark
    template_name = "dashboard/bookmark_update.html"
    fields = ["title", "thumbnail", "content", "url"]
    success_url = reverse_lazy("home")


class DashHome(LoginRequiredMixin, View):
    template_name = "dashboard/home.html"
    context = dict()
    login_url = reverse_lazy("telegram_login")

    def get(self, request):
        user = request.user
        book = Bookmark.objects.filter(author=request.user).order_by("-pub_date")
        self.context["book"] = book
        self.context["first_name"] = user.first_name
        self.context["last_name"] = user.last_name
        self.context["photo_url"] = user.photo_url

        return render(request, "dashboard/home.html", self.context)
