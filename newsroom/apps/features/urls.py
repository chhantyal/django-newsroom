from django.conf.urls.defaults import *
from django.contrib import admin

urlpatterns = patterns('',
    (r'^$', 'features.views.front'),
)
