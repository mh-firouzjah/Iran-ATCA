from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed, pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField

from apps.blog.models import validate_image

DOCUMENT_TYPES = [
    ('articles', _("Articles")),
    ('pdfs', _("PDFs")),
    ('videos', _("Videos")),
    ('voices', _("Voices")),
    ('others', _("Other formats"))
]

STATUS_CHOICES = (('draft', _('Draft')),
                  ('published', _('Published')),)

YES_NO = [(False, _("No")), (True, _("Yes"))]


@receiver(pre_delete, sender="documents.Document")
def update_doc_type_delete(**kwargs):
    document = kwargs['instance']
    cat_list = document.categories.values_list('id', flat=True)
    for cat in DocumentCategory.objects.filter(id__in=cat_list):
        if isinstance(cat.total_documents, int):
            if cat.total_documents > 1:
                cat.total_documents -= 1
        else:
            cat.total_documents = 0
        cat.save()


def get_upload_to(instance, filename):
    return 'upload/documents/%s/%s' % (
        slugify(instance.title, allow_unicode=True),
        filename)


class DocumentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def active(self):
        return super().get_queryset().filter(status='published',
                                             publish__lte=timezone.now())


class Document(models.Model):
    """Model definition for Document."""

    title = models.CharField(_("Title"), max_length=250,
                             db_index=True, unique=True)
    description = models.TextField(_("Description"))
    slug = models.SlugField(verbose_name=_("Slug"), allow_unicode=True,
                            unique_for_date='created')
    uploaded_by = models.ForeignKey("users.AirTrafficController",
                                    verbose_name=_("Uploaded by"),
                                    null=True, on_delete=models.SET_NULL)
    document_type = models.CharField(_("Type"), choices=DOCUMENT_TYPES,
                                     default="no_file", max_length=50)
    categories = models.ManyToManyField("documents.DocumentCategory",
                                        related_name="categorized_documents",
                                        verbose_name=_("Categories"))
    cover = ImageField(verbose_name=_("Cover"), validators=[validate_image, ])
    document_file = models.URLField(_("Download link"),
                                    max_length=200, null=True, blank=True,
                                    help_text=_("If file is uploaded on hosts"))
    content = RichTextUploadingField(verbose_name=_("Content"), null=True, blank=True)
    publish = models.DateTimeField(_("Publish"), default=timezone.now)
    status = models.CharField(verbose_name=_("Status"), choices=STATUS_CHOICES,
                              default='draft', max_length=10)
    created = models.DateField(_("Created"), auto_now_add=True)
    updated = models.DateField(_("Updated"), auto_now=True)

    objects = DocumentManager()

    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        """Meta definition for Document."""

        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ('-publish',)
        indexes = [GinIndex(fields=['search_vector'])]

    def __str__(self):
        """Unicode representation of Document."""
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
        self.search_vector = \
            SearchVector('title_fa', 'title_en',
                         'description_fa', 'description_en', weight='A') + \
            SearchVector('content_fa', 'content_en', weight='B')
        return super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.content is None and self.document_file is None:
            raise ValidationError(
                _('At least one of "Content" or "Download link" must have value'))

    def get_absolute_url(self):
        return reverse('documents:document_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])


class DocumentCategory(models.Model):
    """Model definition for DocumentCategory."""

    title = models.CharField(_("Title"), max_length=250, db_index=True, unique=True,
                             help_text=_("categories e.g: Education, ATC docs,..."))
    total_documents = models.PositiveSmallIntegerField(_("Total Documents"), default=0,
                                                       null=True, blank=True)

    class Meta:
        """Meta definition for DocumentCategory."""

        verbose_name = _('Document Category')
        verbose_name_plural = _('Document Categories')

    def __str__(self):
        """Unicode representation of DocumentCategory."""
        return self.title


def doc_cat_update(sender, instance, action, *args, **kwargs):
    document = instance
    cat_list = document.categories.values_list('id', flat=True)

    if action == 'post_add':
        for cat in DocumentCategory.objects.filter(id__in=cat_list):
            if not isinstance(cat.total_documents, int):
                cat.total_documents = 1
            else:
                cat.total_documents += 1
            cat.save()


m2m_changed.connect(doc_cat_update, sender=Document.categories.through)
