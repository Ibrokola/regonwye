from __future__ import absolute_import, unicode_literals
from datetime import date
from django import forms

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey

class HomePageRelatedLink(Orderable):
    page = ParentalKey('HomePage', related_name='related_links')
    name = models.CharField(max_length=255,null=True, blank=True)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]


class HomePage(Page):
    heading = models.CharField(max_length=200, null=True, blank=True)
    sub_heading = models.CharField(max_length=200, null=True, blank=True)
    intro = RichTextField(blank=True)
    landing_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+' 
    )
    # body = RichTextField(blank=True)

    serach_fields = Page.search_fields + [
        index.SearchField('heading'),
        index.SearchField('sub_heading'),
        index.SearchField('intro')
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('heading'),
            FieldPanel('sub_heading'),
            FieldPanel('intro', classname='full intro'),
            ImageChooserPanel('landing_image'),

        ], heading="Homepage Landing information"),

        InlinePanel('related_links', label="Related links")
    ]

HomePage.promote_panels = Page.promote_panels
