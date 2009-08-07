from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
from account.openid_consumer import PinaxConsumer

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^asu_news21/', include('asu_news21.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    # (r'^$', direct_to_template, {'template': 'front.html'}),
    (r'^$','news21_com.views.front'),
    (r'^search/', direct_to_template, {'template': 'search.html'}),
    (r'^openid/(.*)', PinaxConsumer()),
    (r'^stories/', include('stories.urls.publication')),
    (r'^profiles/', include('basic_profiles.urls')),
    (r'^account/', include('account.urls')),
    (r'^photos/',include('photos.urls')),
    (r'^videos/',include('videos.urls')),
    (r'^about/',include('about.urls')),
    (r'^feeds/', include('feeds.urls')),
    (r'^test/','news21_com.views.test_homepage'),
    (r'^promos/',include('promos.urls')),
    (r'^topics/$', 'news21_com.views.topics_page'),
    (r'^topics/list/$', 'news21_com.views.topics_list'),
    (r'^topics/(?P<slug>[-\w]+)/$', 'news21_com.views.topic_detail'),
    (r'^topics/feed/$', 'news21_com.views.topic_feed'),
    (r'^topics/feed/(.*)$', 'news21_com.views.topic_feed_detail'),
    (r'^about/history/','news21_com.views.about_history'),
    (r'^schools/$','news21_com.views.school_list'),
    (r'^schools/(?P<slug>[-\w]+)/$', 'news21_com.views.school_detail'),
    (r'^about/history/','news21_com.views.about_history'),
    (r'^initiative/$','news21_com.views.initiative'),
    (r'^initiative/curriculum/$','news21_com.views.initiative_curriculum'),
    (r'^initiative/news21/$','news21_com.views.initiative_news21'),
    (r'^initiative/news21/abcnews/$','news21_com.views.initiative_abcnews'),
    (r'^initiative/participants/$','news21_com.views.initiative_participants'),
    (r'^initiative/vision/$','news21_com.views.initiative_vision'),
    (r'^taskforce/$','news21_com.views.taskforce'),
    (r'^taskforce/manifesto/$','news21_com.views.taskforce_manifesto'),
    # keep this url for Gannet, until things change for good
    (r'^topic_feed/(.*)$', 'news21_com.views.topic_feed_detail')
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('', 
        (r'^site_media/(?P<path>.*)$', 'staticfiles.views.serve')
    )
