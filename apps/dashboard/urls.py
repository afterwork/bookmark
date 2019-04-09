from django.conf.urls import include
from django.urls import path
from . import views


urlpatterns = [
    path("", views.DashHome.as_view(), name="home"),
    path("create/", views.BookmarkFormView.as_view(), name="create_bookmark"),
    path("delete/<int:pk>", views.BookmarkDeleteView.as_view(), name="delete_bookmark"),
]
