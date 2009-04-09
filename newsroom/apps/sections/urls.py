from django.conf.urls.defaults import *
from sections import views

urlpatterns = patterns('',
        url(r'^$',
            views.sections_list,
            name='sections_section_list'),
        url(r'^(?P<id>\d+)/$', 
            views.section_detail,
            name='sections_section_detail'),
        url(r'^add/$',
            views.section_add,
            name='section_section_add'),
        url(r'^(?P<id>\d+)/edit/$',
            views.section_edit,
            name='sections_section_edit'),
)

