from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactUs


class ContactUsForm(forms.ModelForm):
    """simple form to perform ContactUs."""

    class Meta:
        model = ContactUs
        exclude = ('client_ip',)
    name = forms.CharField(label=_("Your Name"), max_length=250, required=True,
                           widget=forms.TextInput())
    email = forms.EmailField(label=_("Your Email"), required=True,
                             widget=forms.EmailInput())
    subject = forms.CharField(label=_("Subject"), max_length=250, required=True,
                              widget=forms.TextInput())
    content = forms.CharField(label=_("Your Message"),
                              required=True, widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs.update(
            {'class': 'md-textarea form-control',
                'rows': '3'})
