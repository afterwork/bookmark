from .models import Bookmark
from django import forms
from django.core.validators import URLValidator, RegexValidator
from django.core.exceptions import ValidationError


class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ["title", "thumbnail", "content", "url"]

    def clean_title(self):
        title = self.cleaned_data.get("title", False)
        if len(title.split()) < 2:
            raise forms.ValidationError("Title should contain at least 2 words")
        return title
