# Introduction #

[django\_inlines](http://github.com/mintchaos/django_inlines/tree/master) is a reusable app that allow you to include other objects and special bits in your text fields (models.TextField).

I am going to illustrate this by using a concrete example let us imagine that we want to add a photo inside the page.content related to a story. The interesting part of this is that the photo will then be displayed "inline".

# Details #

Here it is the step by step operation you will need to follow to do this :
  * Create a story => http://localhost:8000/newsroom/story/add/
  * go into the admin interface to add a page to this story in the content field you should add some text and inline you will add this tag '<% photo 1 width=100 height=100 %>'. This tag will display the photo id=1 with the width and height specified. The photo will be displayed using this template "newsroom\_project/templates/inlines/photo.html"
  * View your story http://localhost:8000/publication/2/story-slug/page/1/