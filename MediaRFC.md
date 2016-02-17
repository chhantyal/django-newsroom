# Introduction #

The goal is to create a flexible system that is easy to use and easy to understand. It is not the goal of this project to invent new ways of managing the individual media types within the system since there are already several usable open source apps available for many common publishing media types. For example, Photologue already provides solid tools for managing photos (images) and galleries. In this case the Media app is providing a thin wrapper around the Photologue Photo model. Photo consumers can still take advantage of the Photologue API when needed, but should be able to use the simple Media API in most cases. It probably makes sense to decide on a reasonable set of defaults for each media type and expose those in a consistent manner through the API, further reducing the need to drop lower than the Media API.


# Details #

As of [r205](https://code.google.com/p/django-newsroom/source/detail?r=205) a working proof-of-concept was committed. There is no supporting UI yet, I've tested by manually performing some steps. Please refer to multimedia.models for additional documentation.

## Overview ##

Media is the parent model (base class) for media types within newsroom. Generally, your application will never create instances of Media; rather you will work with instances of the derived classes.

### API ###
**render**

Every subclass must implement the `render()` method. The render method returns the HTML string that will be placed into the page to render the media item in-place.

**get\_insert\_snippet**

Subclasses may also choose to override `get_insert_snippet` if they need to accept additional arguments specific to the media type they represent. _Note that the media\_insert template tag needs to be updated to handle arbitrary arguments first_
_See also Handling Config/Options below_

### Example ###

  1. user creates new Story
  1. while editing Page 1, user selects Add Image
  1. user would select from existing/available photos or add new
  1. when they've selected photo, view should create a new multimedia.models.Image object and set the Image.content\_object to the photo.
  1. view would then add the Image to the Page's media
  1. call get\_insert\_snippet on the image to provide an insert snippet for the author to use where they'd like the media to render.

```
#selected_photo is the photologue Photo instance representing an image selected for
#add by the user
image = Image()
image.content_object = selected_photo
#set title,description fields....
image.save()
page.media.add(image)
insert_snippet = image.get_insert_snippet()
```

## Handling Config/Options for Individual Media Types ##

In general it would be desirable for insert snippets to be as terse as possible; enough to convey to the author that a media item will show up there and which one it will be. I like the idea of preserving the ability to explicitly send in extra parameters when needed, but I think it makes sense to treat those as rare cases. One idea I had was to create another model that would be used to hold individual options (ex: height,width,startFrame,etc...) which would then be associated with the Media objects. Then during render time the Media object would check for an associated Options object and use the values there. Another attractive approach is to simply add an options field onto Media models and pickle any options in there.

The primary use case for this is UI that would expose the properties available for the media type when the user is selecting from inventory for adding a story and the user would be able to customize the options inline.

## Embeddable Blocks and Media Object Types ##

The site should be able to accommodate embedding code "widgets" from other sites and integrating content with APIs from other sites.

Embedding these html widgets should be easily accomplished by authors. The same technology that goes into embedding these blocks of code also applies to embedding media.  We will be collectively calling these objects and the app that makes this all possible "blocks"

A few expected blocks are:

  * Images local to News21 / Slideshow local to News21
  * Flickr Slideshow / Flickr image
  * Tables / Excel Spreadsheets (graphs?)
  * YouTube Video from News21 Account / YouTube video from other accounts / Video local to News21?
  * SoundSlides multimedia / Flash widgets
  * Google Maps
  * Slideshare presentation
  * Audio ?
  * PDF/Word files
  * Links
  * TagClouds
  * Etc.

Integrating APIs should be easily accomplished by developers with the ability to hand off a block that performs a specific function to authors so that they can easily, say, add data to the web site and have it interact with an api from another source and display the information they are looking for (I realize this is vague or simplified, but it’s a foot in the door).


## Media Tab ##

When a person goes to the media tab that is global to the entire site:

  * they will see a list of media
  * they will be able to edit the media on this page
  * they will NOT be able to ADD media from this page

## Adding Media ##

Media is added through Stories (and possibly other objects, like promos, TBD).

To Add Media

  1. First Add a Story
  1. Fill in the metadata, click Save
  1. Click on the Media Tab
  1. Under the Media Tab you will see a list of media:
    * that is particular to the current story
    * that is has been added by the current user (across all stories/promos etc).
    * Media could also be listed according social relationships using the pinax friends app.  So, if someone is your friend then you can see their media.
    * you may have the option to see a paged list of media in alphabetical order that has been added across all users across the entire site.
    * you may have the option to browse a gallery of rights cleared images
  1. To add new media, click on the links under the Action Tab to add video or image (and other types to come)
  1. This newly added media object will also gain an association with the story in which it was uploaded.
  1. A media object can be used across many different stories (or perhaps other object types, like promos)

## The Media Tag ##

Media Tags will be used, behind the scenes.  The author will not know the difference either way, as they will be editing the story visually.

The raw, rendered html will only be present:
  * in the visual editor and
  * in the published story as it is served to the visitor.