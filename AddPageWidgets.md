#How to enable page widgets

# Introduction #

This page will describe how to add page widgets to the page editor, in order to enable the editing interface.


# Details #

Page widgets are a set of predefined html tied with javascript to enable dynamic edition of html content. Page widgets rely heavily on javascript/ajax to work, and it's relatively easy to add new ones.

In order to create a new page widget, markup must be defined. Here is the example of the image widget:
```
<div class="widget-block widget-image-block">
    <img width="100%" height="300" src=""/>
</div>
```

The magic here is in the class attribute for the the div. By specifying "widget-image-block" we are enabling specific behaviour to occur for these type of "objects".
In order to enable an editing interface for the widget, two files are needed:
  * pages.js
  * widget.class.js


## pages.js ##
This is the js handler for events. Is is where events are binded to enable specific actions on specific widgets. For example, to change images on an image widget, we do this:
```
// image widget events
$(".widget-image-block").live("click",function(){
    var widget_obj = $(this);
    widget.image_change(widget_obj);
    return false;
});
```
This will bind the click event to a function in the widget class. For simplicity, and because there are not many widgets yet, a single class was created to handle functionality (show image gallery + change select image).


## widget.class.js ##
This is the code to handle the image\_change call on pages.js:

```
    image_change : function(widget_obj){

        function callback_init()
        {
            $("#ajax-media-list").load(page_media_source_url,function(){

                $("#ajax-media-list .media-item").click(function(){
                    var media_url = $(this).attr("href");
                    widget_obj.children("img").attr("src",media_url);
                    return false;
                });

            });
            return true;
        };

        widget.lightbox(page_media_list_url,callback_init);
        return false;
    },
```

Some explanation:
This function triggers widget.lightbox() which is used to render a lightbox and takes a url and a callback function as parameters.
In this example the url is in variable _page\_media\_list\_url_ which is defined in story\_page\_list.html to enable dynamic urls (please avoid hard coding urls in javascript when they can be dynamic)
```
var page_media_list_url = "{% url stories_page_templates "media_list" %}?width=750&height=500";
```

After this url is loaded, the callback function is executed. The purpose of this callback function is to load objects and handle it's functionality. In this case we are loading a list of images, and binding a click event to each one of them. In this click event we will make the appropriate changes to variable _widget\_object_, which is the image widget that was called on the ui, and that we can change.