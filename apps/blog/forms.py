from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment


class CommentForm(forms.ModelForm):
    """Form for the Comment model"""
    class Meta:
        model = Comment
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update(
            {'class': 'form-control',
             'style': 'width: 100% !important;'}
        )


class SearchForm(forms.Form):
    query = forms.CharField(help_text=_(
        "if the term was not found, we will check for similar terms"))

    check_for_similarities = forms.BooleanField(
        label=_('Check for similar terms'),
        required=False, initial=False,
        help_text=_("may cause heavy loading and more delay"))
    consider_one_phrase = forms.BooleanField(label=_('Consider as single phrase'),
                                             required=False, initial=False,
                                             help_text=_("this will reduse search time"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['query'].widget.attrs.update(
            {'placeholder': _('Search'),
             'class': 'form-control form-control-sm', })
        for item in ['check_for_similarities', 'consider_one_phrase']:
            self.fields[item].widget.attrs.update(
                {'class': 'form-check-input filled-in'})
        return
