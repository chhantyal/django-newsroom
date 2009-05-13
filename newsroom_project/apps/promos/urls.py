from django.conf.urls.defaults import *
from django.contrib import admin
from promos import views

urlpatterns = patterns('',

    url(r'^$', 
        views.promo_list,
        name="promos_promo_list"),

    url(r'^add/$', 
        views.promo_add,
        name="promos_promo_add"),

    url(r'^(?P<id>\d+)/edit/$',
        views.promo_edit,
        name='promos_promo_edit'),

    url(r'^(?P<id>\d+)/$', 
        views.promo_detail,
        name="promos_promo_detail"),
    
    url(r'^image_add/$', 
        views.promo_image_add,
        name="promos_promo_image_add"),    

    url(r'^link_add/$', 
        views.promo_link_add,
        name="promos_promo_link_add"),
    
)
