from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import ImageField

from apps.blog.models import validate_image

numeric = RegexValidator(r'^[0-9+]',
                         _('Please enter numbers, or switch your keyboard to `en`.'))

YES_NO = [(False, _("No")), (True, _("Yes"))]


class Company(models.Model):

    name = models.CharField(_("Name"), max_length=254)
    logo = ImageField(verbose_name=_('Logo'),
                      upload_to='logo/',
                      validators=[validate_image, ])
    short_description = RichTextField(verbose_name=_('Short Description'),
                                      config_name='toolbar_basic')
    long_description = RichTextField(verbose_name=_('Long Description'))
    footer_description = RichTextField(verbose_name=_('Footer Description'),
                                       config_name='toolbar_basic')
    timetable_intro = RichTextField(verbose_name=_('Timetable intro'),
                                    config_name='toolbar_basic')
    contact_intro = RichTextField(verbose_name=_('Contact us intro'),
                                  config_name='toolbar_basic')
    phone1 = models.CharField(_("Phone (main)"), max_length=11,
                              validators=[numeric, ])
    phone2 = models.CharField(_("Phone"), max_length=11,
                              validators=[numeric, ], null=True, blank=True)
    fax = models.CharField(_("Fax"), max_length=11,
                           validators=[numeric, ])
    email = models.EmailField(_("Email"), max_length=254)
    address = models.CharField(_("Address"), max_length=254)
    social_links = models.ManyToManyField("company.CompanySocialLink",
                                          verbose_name=_("Social Links"))
    darken_logo = models.BooleanField(_("Darken Logo"), default=False, choices=YES_NO)

    class Meta:
        verbose_name = _("Iran-ATCA")
        verbose_name_plural = _("Iran-ATCA")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("Company_detail", kwargs={"pk": self.pk})


class CompanySocialLink(models.Model):
    """Model definition for CompanySocialLink."""

    title = models.CharField(_("Title"), max_length=50)
    url = models.URLField(_("URL"), max_length=200)
    icon = models.CharField(_("icon"),
                            help_text=_("An icon-tag from fontawesome.com"),
                            max_length=250)

    class Meta:
        """Meta definition for CompanySocialLink."""

        verbose_name = _('Company Social Link')
        verbose_name_plural = _('Company Social Links')

    def __str__(self):
        """Unicode representation of CompanySocialLink."""
        return str(self.url)


class UsefulLink(models.Model):

    title = models.CharField(_("Title"), max_length=254)
    url = models.URLField(_("URL"), max_length=200)

    class Meta:
        verbose_name = _("Useful Link")
        verbose_name_plural = _("Useful Links")

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("UsefulLink_detail", kwargs={"pk": self.pk})


class ManagementTeam(models.Model):
    """Model definition for ManagementTeam."""

    intro = RichTextField(verbose_name=_("Introduction"))
    secretary_general = models.ForeignKey('users.AirTrafficController',
                                          verbose_name=_("Secretary-General"),
                                          related_name="managed_teams",
                                          on_delete=models.CASCADE)
    veep = models.ForeignKey('users.AirTrafficController',
                             verbose_name=_("Veep"),
                             related_name="veeped_teams",
                             on_delete=models.CASCADE)
    treasure = models.ForeignKey('users.AirTrafficController',
                                 verbose_name=_("Treasure"),
                                 related_name="treasured_teams",
                                 on_delete=models.CASCADE)
    warden = models.ForeignKey('users.AirTrafficController',
                               verbose_name=_("Warden"),
                               related_name="wardend_teams",
                               on_delete=models.CASCADE)
    headPR = models.ForeignKey('users.AirTrafficController',
                               verbose_name=_("Head of PR"),
                               related_name="headPR_teams",
                               on_delete=models.CASCADE)
    headFR = models.ForeignKey('users.AirTrafficController',
                               verbose_name=_("Head of FR"),
                               related_name="headFR_teams",
                               on_delete=models.CASCADE)
    secretary = models.ForeignKey('users.AirTrafficController',
                                  verbose_name=_("Secretary"),
                                  related_name="secretary_teams",
                                  on_delete=models.CASCADE)


    class Meta:
        """Meta definition for ManagementTeam."""

        verbose_name = _('Management Team')
        verbose_name_plural = _('Management Teams')

    def __str__(self):
        """Unicode representation of ManagementTeam."""
        return '{}'.format(self.intro)



class TimetableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def active(self):
        return self.get_queryset().filter(date__gte=timezone.now())


class Timetable(models.Model):
    """Model definition for Timetable."""

    name = models.CharField(verbose_name=_("Name"), max_length=250)
    date = models.DateTimeField(verbose_name=_("Date"))
    public = models.BooleanField(_("Public"), default=False, choices=YES_NO)
    description = RichTextField(verbose_name=_('Description'),
                                config_name='toolbar_basic')
    content = RichTextField(verbose_name=_('Content'), null=True, blank=True)
    created = models.DateField(_("Created"), auto_now_add=True)
    updated = models.DateField(_("Updated"), auto_now=True)

    objects = TimetableManager()

    class Meta:
        """Meta definition for Timetable."""

        verbose_name = _('Timetable')
        verbose_name_plural = _('Timetables')
        ordering = ('-date',)

    def __str__(self):
        """Unicode representation of Timetable."""
        return self.name

    def get_absolute_url(self):
        return reverse("company:timetable_detail", kwargs={"id": self.id})


class ContactUs(models.Model):
    """Model definition for ContactUs."""

    name = models.CharField(_("Name"), max_length=250)
    email = models.EmailField(_("Email"), max_length=254)
    subject = models.CharField(_("Subject"), max_length=250)
    content = models.TextField(_("Content"))
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    client_ip = models.GenericIPAddressField(
        _("ClientIP"), protocol="both", unpack_ipv4=False)

    class Meta:
        """Meta definition for ContactUs."""

        verbose_name = _('Contact Us')
        verbose_name_plural = _('Contact Us')

    def __str__(self):
        """Unicode representation of ContactUs."""
        return self.name
