from __future__ import absolute_import, unicode_literals
from datetime import date
from django import forms

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey




class FormIndexPage(Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    index_title = models.CharField(max_length=300, null=True, blank=True)
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('index_title'),
        index.SearchField('intro')
    ]


    def get_context(self, request):
        context = super(FormIndexPage, self).get_context(request)
        formpages = self.get_children().live().order_by('-first_published_at')
        return context


    content_panels = Page.content_panels + [
        # FieldPanel('title', classname='full title'),
        ImageChooserPanel('header_image'),
        FieldPanel('index_title'),
        FieldPanel('intro', classname='Forms Intro')
    ]


class FormPageRelatedLink(Orderable):
    page = ParentalKey('FormPage', related_name='forms_link')
    name = models.CharField(max_length=300, null=True, blank=True)
    url = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]



class FormPage(Page):
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    form_title = models.CharField(max_length=300, null=True, blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    search_fields = Page.search_fields + [
        index.SearchField('form_title'),
    ]


    content_panels = Page.content_panels + [
        ImageChooserPanel('main_image'),
        FieldPanel('form_title'),
        ImageChooserPanel('feed_image'),
        InlinePanel('forms_link', label='Links to forms')
    ]
