from django.conf.urls.defaults import *
from topics import views

urlpatterns = patterns('',
        url(r'^$',
            views.topics_list,
            name='topics_topic_list'),
        url(r'^(?P<id>\d+)/$', 
            views.topic_detail,
            name='topics_topic_detail'),
        url(r'^add/$',
            views.topics_add,
            name='topics_topic_add'),
        url(r'^(?P<id>\d+)/edit/$',
            views.topic_edit,
            name='topics_topic_edit'),
        url(r'^path/$',
            views.topic_path_list,
            name='topics_topic_path_list'),
        url(r'^path/add/$',
            views.topic_path_add,
            name='topics_topic_path_add'),
        url(r'^path/(?P<id>\d+)/edit/$',
            views.topic_path_edit,
            name='topics_topic_path_edit'),
)

