from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import Truncator, slugify
from django.utils.translation import gettext_lazy as _
# from hitcount.models import HitCount
from jalali_date import datetime2jalali
from sorl.thumbnail import ImageField

STATUS_CHOICES = (('draft', _('Draft')),
                  ('published', _('Published')),)

YES_NO = [(False, _("No")), (True, _("Yes"))]


class PostCategory(models.Model):
    name = models.CharField(_("Name"), max_length=250, unique=True)
    slug = models.SlugField(_("Slug"), allow_unicode=True)
    icon = models.CharField(_("icon"),
                            help_text=_("An icon-tag from fontawesome.com"),
                            null=True, blank=True,
                            max_length=250)

    class Meta:
        verbose_name = _("Post Category")
        verbose_name_plural = _("Post Categories")

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published',
                                             publish__lte=timezone.now())


class PublicManager(PublishedManager):
    def get_queryset(self):
        return super().get_queryset().filter(public=True)


class Post(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=250)
    slug = models.SlugField(verbose_name=_("Slug"), allow_unicode=True,
                            unique_for_date='publish')
    descrip = models.CharField(verbose_name=_("Description"), max_length=254,
                               null=True, blank=True)
    categories = models.ManyToManyField("blog.PostCategory",
        help_text=_("Type comma to create a new instance."),
        verbose_name=_("Categories"),
        related_name='categorized_posts')
    author = models.ForeignKey('users.AirTrafficController', verbose_name=_("Author"),
                               related_name='blog_posts', null=True, blank=False,
                               db_index=True, on_delete=models.SET_NULL)
    body = RichTextUploadingField(verbose_name=_("Body"), )
    publish = models.DateTimeField(verbose_name=_("Publish"),
                                   default=timezone.now)
    created = models.DateTimeField(verbose_name=_("Created"),
                                   auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("Updated"),
                                   auto_now=True)
    status = models.CharField(verbose_name=_("Status"),
                              max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    public = models.BooleanField(verbose_name=_("Public"),
                                 choices=YES_NO,
                                 default=False)
    international = models.BooleanField(_("International"), default=False, choices=YES_NO)
    tags = models.ManyToManyField('blog.Tags',
                                  help_text=_("Type comma to create a new instance."),
                                  verbose_name=_("Tags"), related_name='tagged_posts')

    # hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
    # related_query_name = 'hit_count_generic_relation')

    objects = models.Manager()  # The default manager.
    published = PublishedManager()
    publics = PublicManager()

    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ('-publish',)
        indexes = [GinIndex(fields=['search_vector'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])

    def description(self):
        return self.descrip or strip_tags(Truncator(
            self.body).words(
            254, html=True, truncate=' see more'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
        self.search_vector = \
            SearchVector('title_fa', 'title_en', weight='A') + \
            SearchVector('body_fa', 'body_en', weight='B')
        return super().save(*args, **kwargs)


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


def get_upload_to(instance, filename):
    return 'upload/%s/%s' % (slugify(instance.post.title, allow_unicode=True), filename)


class PostImages(models.Model):
    post = models.ForeignKey("blog.Post",
                             verbose_name=_("Post"),
                             related_name='images',
                             on_delete=models.CASCADE)
    image = ImageField(verbose_name=_("Image"),
                       upload_to=get_upload_to,
                       validators=[validate_image, ])

    class Meta:
        verbose_name = _('Post Image')
        verbose_name_plural = _('Post Images')

    def __str__(self):
        return self.image.url.split('/')[-1]


class CommentManager(models.Manager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def published(self, post):
        return super().get_queryset().filter(post=post, active=True)

    def publics(self, post):
        return super().get_queryset().filter(post=post, active=True, public=True)


class Comment(models.Model):
    user = models.ForeignKey('users.AirTrafficController',
                             verbose_name=_("User"),
                             on_delete=models.CASCADE)
    post = models.ForeignKey("blog.Post",
                             verbose_name=_("Post"),
                             related_name='comments',
                             on_delete=models.CASCADE)
    replied = models.ForeignKey("self",
                                verbose_name=_("Replied to"),
                                related_name='replies',
                                null=True, blank=True,
                                on_delete=models.SET_NULL)
    content = RichTextField(verbose_name=_('Content'), config_name='toolbar_comment')
    created = models.DateTimeField(verbose_name=_("Created"),
                                   auto_now_add=True)
    active = models.BooleanField(_("Active"),
                                 choices=YES_NO,
                                 default=True)
    public = models.BooleanField(verbose_name=_("public"),
                                 choices=YES_NO,
                                 default=False)
    publish = models.DateTimeField(verbose_name=_("Publish"),
                                   auto_now=True)

    objects = CommentManager()


    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ('created', )

    def __str__(self):
        date = datetime2jalali(self.created).strftime('%y/%m/%d')
        return _('{self_user} to {self_post} on {self_created}').format(
            self_user=self.user, self_post=self.post, self_created=date)


class HitCount(models.Model):
    """Model definition for HitCount."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for HitCount."""

        verbose_name = _('Hit Count')
        verbose_name_plural = _('Hit Count')

    def __str__(self):
        """Unicode representation of HitCount."""
        pass
