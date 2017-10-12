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



class PersonPageRelatedLink(Orderable):
    page = ParentalKey('PersonPage', related_name='related_links')
    name = models.CharField(max_length=255,null=True, blank=True)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]


class PersonPage(Page):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    intro = models.TextField(blank=True)
    biography = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
        index.SearchField('intro'),
        index.SearchField('biography'),
    ]

PersonPage.content_panels = [
    FieldPanel('first_name'),
    FieldPanel('last_name'),
    FieldPanel('intro'),
    FieldPanel('biography', classname="Person's biography"),
    ImageChooserPanel('image'),
    InlinePanel('related_links', label="Other links to be added")
]
PersonPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]