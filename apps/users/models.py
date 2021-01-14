from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import timesince
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

YES_NO = [(False, _("No")), (True, _("Yes"))]

GENDER = [('male', _('Male')), ('female', _('Female'))]

SOCIAL_APPS_ICONS = [
    ('<!--Facebook-->'
        '<a href="%(link)s" type="button" title="Facebook" '
        'class="btn-floating btn-large btn-fb">'
        '<i class="fab fa-facebook-f"></i>'
        '</a>', _("Facebook")),


    ('<!--Twitter-->'
        '<a href="%(link)s" type="button" title="Twitter" '
        'class="btn-floating btn-large btn-tw">'
        '<i class="fab fa-twitter"></i>'
        '</a>', _("Twitter")),

    ('<!--Instagram-->'
        '<a href="%(link)s" type="button" title="Instagram" '
        'class="btn-floating btn-large btn-ins">'
        '<i class="fab fa-instagram"></i>'
        '</a>', _("Instagram")),

    ('<!--Telegram-->'
        '<a href="%(link)s" type="button" title="Telegram" '
        'class="btn-floating btn-large btn-blue">'
        '<i class="fab fa-telegram-plane"></i>'
        '</a>', _("Telegram")),

    ('<!--Email-->'
        '<a href="%(link)s" type="button" title="Email" '
        'class="btn-floating btn-large btn-email">'
        '<i class="fas fa-envelope"></i>'
        '</a>', _("Email"))]


class User(AbstractUser):
    '''Customize Django Default UserModel'''

    description = RichTextField(verbose_name=_("Description"),
                                null=True, blank=True,
                                config_name='toolbar_comment',
                                max_length=254,
                                help_text=_(
        'This text should be provided for `Author` users.'))
    story = RichTextField(verbose_name=_("Story"),
                          null=True, blank=True,
                          config_name='toolbar_comment',
                          max_length=254)

    def get_absolute_url(self):
        return reverse('users:user_detail',
                       kwargs={'pk': self.pk})

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.username

    def __str__(self):
        return self.get_full_name()


class Group(Group):
    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')


class AirTrafficController(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                verbose_name=_("User"),
                                related_name='atc_info',
                                help_text=_("Choose the who has not been selected yet"),
                                on_delete=models.CASCADE,)
    mobile = models.CharField(_("Mobile"), max_length=15, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=15, null=True, blank=True)
    work_city = models.CharField(_("Work City"), max_length=250, null=True, blank=True)
    father = models.CharField(_("Father"), max_length=250, null=True, blank=True)
    birth = models.DateField(_("Birth"), null=True, blank=True)
    birth_place = models.CharField(_("Birth Place"),
                                   max_length=250, null=True, blank=True)
    gender = models.CharField(_("Gender"), max_length=6, choices=GENDER)
    maried = models.BooleanField(_("Maried"), default=True, choices=[(False, _('Single')),
                                                                     (True, _('Maried'))])
    nationality_code = models.CharField(_("Nationality Code"), max_length=11,
                                        null=True, blank=True)
    member_of_iranatca = models.BooleanField(_("Member Of Iran-ATCA"),
                                             choices=YES_NO, default=True)
    iranatca_code = models.CharField(_("Iran-ATCA code"), max_length=11,
                                     null=True, blank=True)
    member_of_ifatca = models.BooleanField(_("Member of IFATCA"),
                                           choices=YES_NO, default=False)
    ifatca_code = models.CharField(_("IFATCA code"), max_length=11, null=True, blank=True)
    joined = models.DateField(_("Joined"), null=True, blank=True)
    passedaway = models.BooleanField(_("Passed-away"), choices=YES_NO, default=False)
    paid_years = models.TextField(_("Paid membership years"),
                                  help_text=_('Provide a comma separated list'))
    address = models.TextField(_("Address"), null=True, blank=True)
    academic_licenses = models.TextField(_("Academic Licenses"),
                                         null=True, blank=True,
                                         help_text=_('Provide a comma separated list'))

    class Meta:
        verbose_name = _("Air Traffic Controller")
        verbose_name_plural = _("Air Traffic Controllers")
        ordering = ('joined', )

    def __str__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('users:atc_user_detail',
                       kwargs={'pk': self.pk})

    def has_notifications(self):
        return Notification.objects.filter(user=self).exists()


class SocialMedia(models.Model):
    """Model definition for SocialMedia."""

    user = models.ForeignKey("users.AirTrafficController", verbose_name=_("User"),
                             related_name="social_links", on_delete=models.CASCADE)
    user_link = models.URLField(_("Link"), max_length=200, unique=True)
    social_media = models.CharField(_("Media"), choices=SOCIAL_APPS_ICONS, max_length=250)

    class Meta:
        """Meta definition for SocialMedia."""

        verbose_name = _('Social Media')
        verbose_name_plural = _('Social Medias')

    def __str__(self):
        """Unicode representation of SocialMedia."""
        return mark_safe(
            f'{self.social_media % {"link": str(self.user_link)}} - {self.user}')

    def html_tag(self):
        return mark_safe(self.social_media % {'link': str(self.user_link)})


class Notification(models.Model):
    """Model definition for Notification."""

    user = models.ForeignKey("users.AirTrafficController", related_name="notifications",
                             verbose_name=_("user"), on_delete=models.CASCADE)
    event = models.CharField(_("Event"), max_length=250)
    content = RichTextField(verbose_name=_("Content"), null=True, blank=True)
    url = models.CharField(_("URL"), max_length=200, null=True, blank=True)
    acknowledged = models.BooleanField(_("Acknowledged"), default=False)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        """Meta definition for Notification."""
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ('-created', '-updated', )

    def __str__(self):
        """Unicode representation of Notification."""
        string = _("for: {user_name}, event: {event}")
        return string.format(user_name=self.user,
                             event=self.event)


# @receiver(post_save, sender='blog.Comment')
# def notify_comments_to_user(sender, **kwargs):
#     instance = kwargs['instance']
#     rel = instance.replied
#     url = instance.post.get_absolute_url()
#     string = _("{user_name} has commented your post: {post}, at: {time} ago")
#     string = string.format(user_name=instance.user, post=instance.post,
#                            time=timesince(timezone.now()))
#     notification = Notification(user=instance.post.author, event=string, url=url)
#     notification.save()
#     rel = instance.replied
#     if rel:
#         string = _("{user_name} has commented your comment: {rel}, at: {time} ago")
#         string = string.format(user_name=instance.user, rel=rel,
#                                time=timesince(timezone.now()))
#         notification = Notification(user=rel.user, event=string, url=url)
#         notification.save()
#     return
