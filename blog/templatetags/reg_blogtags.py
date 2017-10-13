from datetime import date
from django import template
from django.conf import settings

from blog.models import BlogPage

register = template.Library()



# Blog feed for home page
@register.inclusion_tag('blog/tags/blog_listing_homepage.html',takes_context=True)
def blog_listing_homepage(context, count=3):
    posts = BlogPage.objects.live().order_by('-first_published_at')
    return {
        'posts': posts[:count],
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

# # Article feed for home page
# @register.inclusion_tag('core/tags/homepage_article_listing.html', takes_context=True)
# def homepage_article_listing(context, count=6):
#     article_posts = play_filter(ArticlePage.objects.filter(live=True).order_by('-date'), count)
#     return {
#         'article_posts': article_posts,
#         # required by the pageurl tag that we want to use within this template
#         'request': context['request'],
#     }