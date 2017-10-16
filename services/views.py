from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from .models import ServiceIndexPage, ServicePage, ServiceCategory
from django.shortcuts import get_object_or_404
from django.conf import settings


# def tag_view(request, tag):
#     index = ServiceIndexPage.objects.first()
#     return index.serve(request, tag=tag)


def category_view(request, category):
    index = ServiceIndexPage.objects.first()
    return index.serve(request, category=category)



class LatestEntriesFeed(Feed):
    '''
    If a URL ends with "rss" try to find a matching ServiceIndexPage
    and return its items.
    '''

    def get_object(self, request, service_slug):
        return get_object_or_404(ServiceIndexPage, slug=service_slug)

    def title(self, service):
        if service.seo_title:
            return service.seo_title
        return service.title

    def link(self, service):
        return service.full_url

    def description(self, service):
        return service.search_description

    def items(self, service):
        num = getattr(settings, 'SERVICE_PAGINATION_PER_PAGE', 10)
        return service.get_descendants().order_by('-first_published_at')[:num]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.specific.body

    def item_link(self, item):
        return item.full_url


class LatestEntriesFeedAtom(LatestEntriesFeed):
    feed_type = Atom1Feed


class LatestCategoryFeed(Feed):
    description = "Services"

    def title(self, category):
        return "Service: " + category.name

    def link(self, category):
        return "/service/category/" + category.slug

    def get_object(self, request, category):
        return get_object_or_404(ServiceCategory, slug=category)

    def items(self, obj):
        return ServicePage.objects.filter(
            categories__category=obj).order_by('-date')[:5]

    def item_title(self, item):
        return item.title

def item_description(self, item):
        return item.body