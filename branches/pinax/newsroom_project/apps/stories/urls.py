# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('stories.views',

    #- EDITIING -
    #list stories
    url('^$','story_list',name='stories_story_list'),
    #add story
    url('^story/add/$','add_story',name='stories_add_story'),
    #edit story
    url('^story/(?P<story_id>\d+)/edit/$','edit_story',name='stories_edit_story'),
    #story overview (page list)
    url('^story/(?P<story_id>\d+)/pages/$','story_pages',name='stories_story_pages'),
    #story media overview (media list)
    url('^story/(?P<story_id>\d+)/media/$','story_media',name='stories_story_media'),
    #add page
    url(r'^story/(?P<story_id>\d+)/page/add/$','add_page',name='stories_add_page'),
    #edit page
    url(r'^story/page/(?P<page_id>\d+)/edit/$','edit_page',name='stories_edit_page'),
    #save page - creates or replaces a page
    url(r'^story/(?P<story_id>\d+)/page/save/$','save_page',name='stories_save_page'),
    #add media
    url(r'^story/(?P<story_id>\d+)/media/(?P<media_type>\w+)/add/$','story_add_edit_media',name='stories_story_add_media'),
    #edit media
    url(r'^story/(?P<story_id>\d+)/media/(?P<media_id>\d+)/edit/$','story_add_edit_media',name='stories_story_edit_media'),
    #associate media
    url(r'^story/(?P<story_id>\d+)/media/(?P<media_type>\w+)/select/$','story_select_media',name='stories_story_select_media'),



    # ajax request for adding pages



    # to do, remove this from here probably
    # get an app just for widgets
    url(r'^text_widget/(?P<widget_name>.+)/$','text_widget',name='stories_page_text_widgets'),
    url(r'^media_widget/(?P<media_id>\d+)/$','media_widget',name='stories_page_media_widgets'),
    url(r'^template/(?P<template_name>.+)/$','page_template',name='stories_page_templates'),


    #- PUBLIC  -
    #diplay story
    url('^(?P<slug>[\d\w-]+)/$','story',name="stories_show_story"),
)

