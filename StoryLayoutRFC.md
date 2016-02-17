# Introduction #

Stories are composed of pages and these pages will contain layout information to define how the page is rendered.  At the time of this writing this layout feature only relates to the stories module.

# Templates #

For example, on the backend we start with a set of pre-defined templates for a page:

```
stories/page_base_1col.html
stories/page_base_2col.html
stories/page_base_3col.html
stories/page_base_3col_bigleadart.html
stories/page_base_3col_noart.html
```

Each template will have the required html and css associated with them to create a layout structure for a specific page.

New templates can be installed and should use the available template context and be valid html.  A page in a story might require a special template, for example, and the system should be flexible enough to accommodate that.

# Columns #

Column breaks are a bit of text that you insert in your content to define where new columns should be started.  The interface to define what layout you would like to use is defined by using column break tags.  So within your page if you want a new column you define a column break, like:

```
<!-- column break -->
```

The page view will parse the page content and depending on how many column breaks exist will choose the appropriate base template for rendering.  If there are more than the supported column breaks in a page body the parser will raise an except or ignore it (TODO).

# Grids #

Each of the supported backend templates will be based on a grid layout, like [960.gs](http://960.gs/).  A  photoshop document or image with the grid structure will be provided.  The grid template can be used to mockup your page in photoshop or on paper, as well as providing you with pixel dimensions for your media within the templates.

This should be sufficient for the authors to plan their story layout and have a complete idea of story layout before approaching the CMS with their final and vetted media.

# Examples #

An example editing processes might be:

## Add Media then Arrange Page ##

Recently Marco introduced a javascript page editor.  So one solution to the page layout problem might be solved by javascript.

  1. create your page content in a textarea introducing media tags or column tags into the content textarea.  Introduce different media elemets.
  1. then click save and preview.  the preview screen provides you with each element, text and media as blocks in which you can expand into some constrained layout screen.
  1. when you save the preview, it uses ajax to post data to a view that saves the html.  which is mostly div tags corresponding to whatever grid system we are using.
# the backend also does parsing and strips html we don't allow.
# formatting like bold and italics can be done on the preview screen as well

## Add media in page editor ##

Another option is when a page is edited the sub nav column goes away and a page layout editor appears at a set width, equal to the published site width.  The page editor allows you to add media elements and arrange things, including adding bold/italics and preformatted things like code examples.  Once you are done arranging blocks then click save and the html is posted via ajax to a view that saves it.  A redirect takes you back to the edit screen that displays the html code in the textarea.  You could do any additional tweaks if you like there.  Editing the HTML gives us more control if we need and allows for edge cases where you might want to embed something the layout editor can't handle.  We also do parsing on the back end to strip tags that are not allowed (like javascript?).

**HTML is an important skill to have.**

## Choose layout ##

  1. there is probably a set list of available templates
  1. page edit screen allows you to change your layout providing visual thumbnail of the layout.
  1. page list screen allows you to choose, preview and save different layouts

## Inlines ##

Recently another pluggable was introduced and I'm not sure if this would provide another type of solution.

http://github.com/mintchaos/django_inlines/tree/master


## Process for Pages / Layout ##

  1. after you click on the link to add a story and enter the appropriate metadata
  1. and after you upload all the media elements for your story
  1. you will click on the link to add a page
  1. from here you will be presented with a handful of page layouts upon which to base your page
  1. once you select the visual layout you will like for your page, you will be presented with the page editor
  1. from here you can add either:
    * text blocks
    * or media blocks
  1. (These blocks (formerly known as widgets) are simply divs).  Depending on the object type, you'll be presented with different editing options within the page editor that are appropriate to the content.
  1. These blocks can be arranged in any manner that the author chooses
  1. The author can even add more rows/columns to the layout as he or she sees fit (Milan, we may want to clarify this a bit further).
  1. Some attention will be paid to the ordering of the blocks in the event, down the road, that the content is viewed on a mobile browser so that they can be paged through in a sequential manner.