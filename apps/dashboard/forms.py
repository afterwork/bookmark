from .models import Bookmark
from django import forms


class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ["title", "thumbnail", "content", "url"]
