from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Chat


class ChatForm(forms.ModelForm):
    """Form definition for Chat."""

    class Meta:
        """Meta definition for Chatform."""

        model = Chat
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = _("Your message:")
