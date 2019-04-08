from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.urls import reverse_lazy
from .models import Bookmark
from .forms import BookmarkForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class BookmarkFormView(View):
    form = BookmarkForm()
    context = {"form": form}

    def post(self, request):
        self.form = BookmarkForm(request.POST or None)
        submission = self.form.save(commit=False)
        submission.author = request.user
        if self.form.is_valid():
            self.form.save()
            self.context = {"form": self.form}
        return render(request, "dashboard/bookmark_thank_you.html", self.context)

    def get(self, request):
        return render(request, "dashboard/bookmark_create.html", self.context)


def bookmark_create_view(request):

    form = BookmarkForm(request.POST or None)
    if form.is_valid():
        submission = form.save(commit=False)
        submission.author = request.user
        form.save()

    context = {"form": form}
    return render(request, "dashboard/bookmark_create.html", context)


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
