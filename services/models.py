from __future__ import absolute_import, unicode_literals
from datetime import date
from django import forms

from django.db import models
from django.db.models import Count, Q
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField, StreamBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailsnippets.models import register_snippet

from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey, ParentalManyToManyField




class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"

class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'), ('mid', 'Mid width'), ('full', 'Full width'),
    ))


class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))

class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()

class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"


def get_service_context(context):
    context['all_categories'] = ServiceCategory.objects.all()
    context['root_categories'] = ServiceCategory.objects.filter(
        parent=None,
    ).prefetch_related(
        'children',
    ).annotate(
        service_count=Count('servicepage'),
    )
    return context


class ServiceIndexPage(Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    heading = models.CharField(max_length=500, null=True, blank=True)
    sub_heading = models.CharField(max_length=500, null=True, blank=True)
    body = RichTextField(null=True, blank=True)


    # @property
    # def services(self):
    #     # Get list of service pages that are descendant of this page
    #     services = ServicePage.objects.descendant_of(self).live()
    #     services = services.order_by('-first_published').prefetch_related('categories', 'categories__category')
    #     return services

    def get_context(self, request, category=None, *args, **kwargs):
        context = super(ServiceIndexPage, self).get_context(request, *args, **kwargs)
       
        # services = self.get_children().live().order_by('-first_published_at') #.prefetch_related('categories', 'categories__category')

        services = ServicePage.objects.child_of(self).live().order_by('-first_published_at').prefetch_related('categories', 'categories__category')

        if category is None:
            if request.GET.get('category'):
                category = get_object_or_404(ServiceCategory, slug=request.GET.get('category'))
        if category:
            if not request.GET.get('category'):
                category = get_object_or_404(ServiceCategory, slug=category)
            services = services.filter(categories__category__name=category)

        # Pagination
        page = request.GET.get('page')
        page_size = 10
        if hasattr(settings, 'SERVICE_PAGINATION_PER_PAGE'):
            page_size = settings.SERVICE_PAGINATION_PER_PAGE

        if page_size is not None:
            paginator = Paginator(services, page_size)  # Show 10 services per page
            try:
                services = paginator.page(page)
            except PageNotAnInteger:
                services = paginator.page(1)
            except EmptyPage:
                services = paginator.page(paginator.num_pages)


        context['services'] = services
        context['category'] = category
        context = get_service_context(context)

        return context



    class Meta:
        verbose_name = _('Service index')
    subpage_types = ['services.ServicePage']


    content_panels = [
        FieldPanel('title', classname='full'),
        ImageChooserPanel('header_image'),
        FieldPanel('heading'),
        FieldPanel('sub_heading'),
        FieldPanel('body', classname='service description'),
    ]


@register_snippet
class ServiceCategory(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name=_('Category Name'))
    slug = models.SlugField(unique=True, max_length=250)
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children")
    date = models.DateField(auto_now_add=True, auto_now=False, null=True, blank=True)
    description = RichTextField(blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = _("Service Category")
        verbose_name_plural = _("Service Categories")

    panels = [
        FieldPanel('name'),
        FieldPanel('parent'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError('Parent category cannot be self.')
            if parent.parent and parent.parent == self:
                raise ValidationError('Cannot have circular Parents.')

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            count = ServiceCategory.objects.filter(slug=slug).count()
            if count > 0:
                slug = '{}-{}'.format(slug, count)
            self.slug = slug
        return super(ServiceCategory, self).save(*args, **kwargs)





class ServiceCategoryServicePage(models.Model):
    category = models.ForeignKey(ServiceCategory, related_name="+", verbose_name=_('Category'))
    page = ParentalKey('ServicePage', related_name='categories')
    panels = [
        FieldPanel('category'),
    ]


class RoadTestLink(Orderable):
    page = ParentalKey('ServicePage', related_name='road_tests')
    name = models.CharField(max_length=300, null=True, blank=True)
    url = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]

class ServicePageRelatedLink(Orderable):
    page = ParentalKey('ServicePage', related_name='drivers_guide')
    name = models.CharField(max_length=300, null=True, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    url = models.URLField(null=True, blank=True)
    panels = [
        FieldPanel('name'),
        ImageChooserPanel('image'),
        FieldPanel('url')
    ] 


class ServicePage(Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Header image')
    )
    service_title = models.CharField(max_length=300, null=True, blank=True)
    body = StreamField([
        ('h1', CharBlock(icon="title", classanme="title")),
        ('h2', CharBlock(icon="title", classanme="title")),
        ('h3', CharBlock(icon="title", classanme="title")),
        ('h4', CharBlock(icon="title", classanme="title")),
        ('h5', CharBlock(icon="title", classanme="title")),
        ('h6', CharBlock(icon="title", classanme="title")),
        ('paragraph', RichTextBlock(icon="pilcrow")),
        ('aligned_image', ImageBlock(label="Aligned image", icon="image")),
        ('pullquote', PullQuoteBlock()),
        ('raw_html', RawHTMLBlock(label='Raw HTML', icon="code")),
        ('embed', EmbedBlock(icon="code")),
    ])
    date = models.DateField("Post date")
    service_categories = models.ManyToManyField(ServiceCategory, through=ServiceCategoryServicePage, blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Feed image')
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('service_title'),
        index.SearchField('title'),]

    
    def get_absolute_url(self):
        return self.url


    def get_service_index(self):
        # Find closest ancestor which is a service index
        return self.get_ancestors().type(ServiceIndexPage).last()

    
    def get_context(self, request, *args, **kwargs):
        context = super(ServicePage, self).get_context(request, *args, **kwargs)
        context['services'] = self.get_service_index().serviceindexpage
        context = get_service_context(context)
        return context

    def get_first_four(self):
        pass

    class Meta:
        ordering = ['first_published_at']
        verbose_name = _('Service page')
        verbose_name_plural = _('Services pages')

    parent_page_types = ['services.ServiceIndexPage']

    
ServicePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('service_title'),
    ImageChooserPanel('header_image'),
    FieldPanel('date'),
    InlinePanel('categories', label=_("Categories")),
    StreamFieldPanel('body'),
    ImageChooserPanel('feed_image'),
    InlinePanel('road_tests', label='iframe for road tests'),
    InlinePanel('drivers_guide', label='drivers guide on road test page')
]

