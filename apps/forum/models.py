
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

YES_NO = [(False, _("No")), (True, _("Yes"))]


class ActiveManager(models.Manager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def active(self):
        return super().get_queryset().filter(active=True)


class Forum(models.Model):
    """Model definition for Forum."""
    name = models.CharField(verbose_name=_("Name"), max_length=250, db_index=True)
    description = RichTextField(verbose_name=_("Description"))
    admin = models.ForeignKey('users.AirTrafficController',
                              verbose_name=_("Admin"),
                              related_name='forums_admin',
                              null=True, blank=False,
                              on_delete=models.SET_NULL)
    publish = models.DateTimeField(verbose_name=_("Publish"), default=timezone.now)
    active = models.BooleanField(verbose_name=_("Active"), default=True, choices=YES_NO)
    members = models.ManyToManyField('users.AirTrafficController',
                                     verbose_name=_("Members"),
                                     null=True, blank=True,
                                     related_name="forums_joined")
    invite_link = models.CharField(_("Invite link"), max_length=250,
                                   null=True, blank=True)

    objects = ActiveManager()

    class Meta:
        """Meta definition for Forum."""
        verbose_name = _('Forum')
        verbose_name_plural = _('Forums')
        ordering = ('-publish',)

    def __str__(self):
        """Unicode representation of Forum."""
        return self.name

    def get_absolute_url(self):
        return reverse('forum:room', kwargs={'pk': self.id})

    def generate_invite_link(self):
        link = reverse('forum:join_room',
                       kwargs={'token': get_random_string(48), 'pk': self.pk, })
        self.invite_link = format_html(link)
        return

    def save(self, **kwargs):
        super().save(**kwargs)
        if not self.invite_link:
            self.generate_invite_link()
        return super().save(update_fields=('invite_link',))


class Chat(models.Model):
    """Model definition for Chat."""
    user = models.ForeignKey('users.AirTrafficController',
                             verbose_name=_("User"),
                             related_name="chats",
                             null=True, blank=False,
                             on_delete=models.SET_NULL)
    forum = models.ForeignKey("forum.Forum",
                              verbose_name=_("Forum"),
                              related_name="chats",
                              on_delete=models.CASCADE)
    content = RichTextUploadingField(verbose_name=_("Content"),
                                     config_name='toolbar_basic', db_index=True)
    reply = models.ForeignKey("self",
                              verbose_name=_("Reply"),
                              related_name="replies",
                              null=True, blank=True,
                              on_delete=models.SET_NULL)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)
    active = models.BooleanField(_("Active"), default=True)

    objects = ActiveManager()

    class Meta:
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")
        # get_latest_by = ('-created', )

    def __str__(self):
        return f"{self.user} {self.forum}"
