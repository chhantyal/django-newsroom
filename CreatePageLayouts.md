# How to create page layouts for newsroom

# Introduction #

This page describes how to create new page layouts form newsroom


# Details #

layouts themselves are stored in the database for easier editing, under the **page\_layouts** app. Layouts consist of html built using 960gs CSS grid, example:

```
<div class="story-container">
    <div class="grid_8">
    <% image_widget height=250 %>
    <% text_widget 2 %>
    </div>
    <div class="grid_4">
    <% image_widget height=200 %>
    <% text_widget 3 %>
    </div>
</div>
```


Various inline widgets can be added to the layout itself to reduce visual html. The currents widgets are:
  * text\_widget (<% text\_widget id %>) uses TextWidget model on page\_layouts to allow for different combinations and text formatting.
  * image\_widget (<% image\_widget height=200 %>) is an inline that can receive both width and height as a parameter. If width is not present, it will use width="100%"

New inlines can be created on page\_layout's models.py, to allow for more combinations