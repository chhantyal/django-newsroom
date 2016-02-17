# Introduction #

In order for a page to get rendered in a publication you need:

  1. A page layout consisting of the correct widgets for each part of the page.
  1. avascript to handle the widgets and actually create the proper html that is saved to the database in the page body text field.
  1. All relevant javascript and css used in the page editor need to also be present in the publication site.

Let's go through the process of adding a page layout that supports a video.

# Create the Mockup #

First thing I do is create a mockup page using typical Django templates on the publication site.

  1. modify `templates/stories/publication/page_detail.html` to include a template rather than rendering from the db.  There is a comment block in that file to quickly switch from rendering a page from the db vs including another template.
  1. create the new page mockup code in `templates/page_layouts/example_page_video.html` and play with the parent and include templates until your mockup is loading.
  1. modify the css and html; code the new layout.  try to use existing style page design patterns if possible.   All css for each page layout lives in one file: `media/common/page_layouts.css`, for now.  After you modify this file you should also make sure that the old page layouts didn't break.  Be smart with your CSS and follow the existing patterns relating to CSS selectors.

Here is how my html for the two column inner\_page\_video layout looks:

```
        <div id="inner_page_video" class="story-container">

            <h1 class="headline">headline goes here</h1>

            <div class="grid_4 alpha">

                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. In pharetra ligula sit amet lectus consectetur porttitor. Nulla facilisi. Mauris porta risus id erat dictum scelerisque. Praesent purus diam, molestie sit amet tempus rutrum, euismod ut odio.</p>

                <p>Curabitur hendrerit gravida mi, ac dignissim lectus faucibus non. Pellentesque facilisis sollicitudin dui vel bibendum. Pellentesque ut orci orci. In pulvinar, libero eget scelerisque euismod, turpis metus pellentesque lorem, in interdum lorem magna in dui. Nulla fermentum, est ac tincidunt rhoncus, turpis lacus rutrum diam, at laoreet lorem est in ipsum.</p>

                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. In pharetra ligula sit amet lectus consectetur porttitor. Nulla facilisi. Mauris porta risus id erat dictum scelerisque. Praesent purus diam, molestie sit amet tempus rutrum, euismod ut odio.</p>
            </div>

            <div class="grid_8 omega">

                <div id="placeholder" style="background-color: #ddd;">Get Flash?</div>

                <div class="media_caption">
                    <p>media title: caption goes here describing the media.</p>
                </div>

                <p>Curabitur hendrerit gravida mi, ac dignissim lectus faucibus non. Pellentesque facilisis sollicitudin dui vel bibendum. Pellentesque ut orci orci. In pulvinar, libero eget scelerisque euismod, turpis metus pellentesque lorem, in interdum lorem magna in dui. Nulla fermentum, est ac tincidunt rhoncus, turpis lacus rutrum diam, at laoreet lorem est in ipsum.</p>

            </div>
        </div>
```

# Create the Page Layout Object #

Once you are happy with the raw html version you will need to create a page layout object in the database in the page\_layouts application.  According to the design of the page editor, any part of a page you want editable needs to be represented by a widget.  The widget interacts with javascript and allows content to be managed by the layout tool.  So all the editable parts of your page will be replaced with something like `<% text_widget 1 %>` which corresponds to text\_widget id 1.  The id references different widgets.  Text widgets are initialized in the database and added as needed.

  1. Replace the text with widgets:
```
        <div id="inner_page_video" class="story-container">

            <% text_widget 6 %>

            <div class="grid_4 alpha">
                <% text_widget 1 %>
            </div>

            <div class="grid_8 omega">

                <% video_widget width=620 %>

                <div class="media_caption">
                    <% text_widget 3 %>
                </div>

                <% text_widget 1 %>

            </div>
        </div>
```

  1. Replace the media with widgets.  The video part of your code will require a new widget because inline video is not supported in the page editor yet.

# Create Video Widget Inline #

To complete the video widget so people can add videos to a layout we need to define a django\_inline template and write the javascript that handles the media insertion.

  1. The inline template is usually simple and to make it clickable you need to add the class of "widget-block" to the html container.  So create  file templates/inlines/video\_widget.html and add the following code.  This just gives the user something to click on.
```
    <div class="widget-block widget-video-block" 
             style="width:{{ width }}px; background-color: #eee;">
    Click to select video.
    </div>
```

  1. Then define the inline model that handles the rendering in apps/page\_layouts/models.py:
```
class VideoInline(inlines.TemplateInline):
    """
    Works similarly as image_widget inline from django_inlines perspective.
    The rest is handled with javascript in the page editor.
    """

    help_text = "Configures a video element on the page."

    inline_args = [
        dict(name='height', help_text="In pixels"),
        dict(name='width', help_text="In pixels"),
        ]

    def get_context(self):
        pass

# notice 'video_widget' matches the string used to define the inline tag.
inlines.registry.register('video_widget', VideoInline)
```

  1. Now create a new page\_layout object in the database using the django admin `http://localhost:8000/admin/page_layouts/pagelayout/add/` .

Here's the page layout model as defined in apps/page\_layouts/models.py:
```
class PageLayout(models.Model):

    title = models.CharField(max_length=256)
    html = models.TextField()
    description = models.TextField()
    image = models.ImageField(
                upload_to="images/widgets/page_layouts",                
                help_text="Thumbnail of the layout, 240px wide.  Frist upload new images and then add via svn.")
```

The title should be something like "Intro Page: Lead Quote and Media Popup", the html is the layout code with widget replacement and the image can be anything 240px wide for right now.

# Create Video Widget Javascript Handlers #

Once we have defined all widgets in the layout then we should be able to see it in the editor.  So add a new page in the editor and choose your new layout.  Now we need to add the corresponding javascript to manage the media insertion.  This is handled in two javascript files, `media/js/pages.js and media/js/widget.class.js`.

First add a javascript onclick handler for the widget by using the css class and jquery to select the div you used to define the widget.  Add this to the bottom of `pages.js`:
```
    // handle video widget events
    $(".widget-video-block").live("click",function(){
        var widget_obj = $(this);
        widget.video_set(widget_obj);
        return false;
    });
```

Then define the javascript that processes the onclick event in `media/js/widget.class.js`:

```
    video_set : function(widget_obj){

        function callback_init(){
            $("#ajax-media-list").load(page_media_source_url,function(){
                $("#ajax-media-list .media-item").click(function(){

                    // get the url we will use to render the video object from the href attribute 
                    // of a DOM element with class "render-url" that is present in the media listing
                    var render_url = $(this).siblings('.render-url').attr('href');

                    // log to javascript error log/console, useful for testing and debugging
                    // console.log(render_url);
                    
                    // load the render html into the widget_obj via an ajax request.
                    widget_obj.load(render_url);

                    // now close the lightbox and return false to cancel out the normal click 
                    // response
                    widget.remove_lightbox();
                    return false;
                });
            });
            return true;
        }

        widget.lightbox(page_media_list_url, callback_init);
        return false;
    },
```