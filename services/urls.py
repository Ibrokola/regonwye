from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^tag/(?P<tag>[-\w]+)/', views.tag_view, name="tag"),
    url(r'^category/(?P<category>[-\w]+)/feed/$', views.LatestCategoryFeed(), name="category_feed"),
    url(r'^c/(?P<category>[-\w]+)/', views.category_view, name="category"),
    # url(r'^author/(?P<author>[-\w]+)/', views.author_view, name="author"),
    url(r'(?P<service_slug>[\w-]+)/rss.*/',
        views.LatestEntriesFeed(),
        name="latest_entries_feed"),
    url(r'(?P<service_slug>[\w-]+)/atom.*/',
        views.LatestEntriesFeedAtom(),
name="latest_entries_feed_atom"),
]

