from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from account.openid_consumer import PinaxConsumer

admin.autodiscover()

import os

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {"template": "homepage.html"}, name="home"),
    
    (r'^about/', include('about.urls')),
    (r'^account/', include('account.urls')),
    (r'^openid/(.*)', PinaxConsumer()),
    (r'^profiles/', include('basic_profiles.urls')),
    (r'^notices/', include('notification.urls')),
    (r'^announcements/', include('announcements.urls')),
#    (r'^projects/', include('projects.urls')),
#    (r'^bookmarks/', include('bookmarks.urls')),
    (r'^avatar/', include('avatar.urls')),
    (r'^promos/', include('promos.urls')),
    (r'^affiliates/', include('core.urls')),
    (r'^newsroom/',include('stories.urls.newsroom')),
    (r'^publication/',include('stories.urls.publication')),
    (r'^topics/',include('topics.urls')),
    (r'^videos/',include('videos.urls')),
    (r'^multimedia/',include('multimedia.urls')),


    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    # handles /photos/ and /galleries/
    (r'', include('photologue.urls')),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('', 
        (r'^site_media/(?P<path>.*)$', 'staticfiles.views.serve')
    )