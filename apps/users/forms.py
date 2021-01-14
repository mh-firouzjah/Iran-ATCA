from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from .models import AirTrafficController, SocialMedia, User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name_fa', 'last_name_fa',
                  'first_name_en', 'last_name_en',
                  'story_fa', 'story_en')
        help_texts = {
            'email': _("Required for password reset"),
        }
        widgets = {
            'story_fa': CKEditorWidget(config_name='toolbar_comment',),
            'story_en': CKEditorWidget(config_name='toolbar_comment',)
        },


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        if AirTrafficController.objects.filter(user=self.user).exists():
            self.fields['first_name_fa'].disabled = True
            self.fields['last_name_fa'].disabled = True


class AirTrafficControllerForm(forms.ModelForm):
    """Form definition for AirTrafficController."""
    class Meta:
        """Meta definition for AirTrafficControllerform."""
        model = AirTrafficController
        exclude = ('user', 'gender', 'nationality_code',
                   'member_of_iranatca', 'iranatca_code',
                   'member_of_ifatca', 'ifatca_code',
                   'joined', 'passedaway',
                   'paid_years',)
        widgets = {
            'maried': forms.Select(
                attrs={'class': "mdb-select md-form"})}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if not visible.field == self.fields['maried']:
                visible.field.widget.attrs['class'] = 'form-control'
        for item in ['academic_licenses', 'address']:
            self.fields[item].widget.attrs = {'class': 'md-textarea form-control',
                                              'row': 6}


class SocialMediaForm(forms.ModelForm):
    """Form definition for SocialMedia."""

    class Meta:
        """Meta definition for SocialMediaform."""

        model = SocialMedia
        # exclude = ('user', )
        fields = '__all__'
        widgets = {
            'social_media': forms.Select(
                attrs={'class': "mdb-select md-form"})}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if not visible.field == self.fields['social_media']:
                visible.field.widget.attrs['class'] = 'form-control'


UserSocialMediaFormset = inlineformset_factory(
    parent_model=AirTrafficController,
    model=SocialMedia,
    form=SocialMediaForm,
    exclude=('user',),
    can_delete=True,
    extra=1,
    validate_max=True,
    max_num=5)
