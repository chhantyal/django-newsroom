# Introduction #

Sections are a top level collection of stories groped by topic.  For instance, a section on the site related to the Housing Crisis could list stories based on the following more general topics “housing,” “banking,” “mortgages” and that would live under the site at
```
http://news21.com/sections/energy/
http://news21.com/sections/energy/alternate/wind/
http://news21.com/sections/economy/
http://news21.com/sections/economy/housing-crisis/
```

A publication might want to create/modify sections at any point in time, depending on current events.  This module should provide an editor with the functionality to perform such a task.  There is potential for the Sections module to touch any part of content in the system, or just stories.  At the time of this writing we are focusing on how sections work with stories.

# Section Paths #

A Section Path is a term we are using to describe free-from strings defined by editors or authors that allow you to categorize content.  The strings follow a simple convention using forward slashes.  They look like slugs but do NOT map to a URL. They are used to define a section, which has the URL mapping.

```
/people/george_bush/
/places/europe/france/region/paris/neighborhood
/topics/immigration
/events/2009/inauguration
```

Section paths should be unique strings within the table, and can be added by authors as needed.

# Sections Editor/Manager #

The Sections Editor provides an interface for, creating new Section Paths and Sections and streamlining editing functions like re-assigning section\_paths in bulk.

# Section Page #

Each section will define a single page, which represents features related to the section, similar to the front page.  Template options will be given, similar to story pages.  Likely a separate set of templates is necessary for section pages, they have different layout requirements than story pages.

# Schema #

```
section (n) ---- (n) section_path (n) ---- (n) stories
```


# Models #

```
class SectionPath(models.Model):

    section_path = models.CharField(max_length=256)


class Section(models.Model):

    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    collection = models.ManyToManyField(SectionPath) 
        
```


# Template Tags #

Within the templates, there might be a need to access arbitrary content based on section path. For example, on the /economy/ page, it would be cool to be able to put in a “Housing Crisis” sidebar that pulls in the appropriate content with something like:

```
{% for get_stories_by_section /economy/housing-crisis/ as story %}
   <a href="{{story.get_absolute_url}}">{{story}}</a>
{% endfor %}
```

# Stories Example #

In this example a screen provides you with a list of checkboxes to relate a story to one or more Section Paths.

Here is a mockup:

http://api.ning.com/files/nLWRHw63e1aqEa0KxR8LNjowx5MawoaxBozi7nKW30c1X6Nc-SDeta-sOC0Yovimz60dJXz-Xtu3UTjOD2NxM7E5A59VlJVf/photo.jpg?width=737&height=552

# Request example #

Description here...

```
GET /economy/housing-crisis/
```

# view #

```
def section_index(request, section_slug=None):
    ...
    stories = Story.objects.filter( section=Section.objects.get(slug=section_slug) )
    ...
```

# Sections vs Projects #

After some conversation it was decided that sections are not project landing pages. The project landing page, also known as project front page, will be a separate page type object attached to a project in the db. So there will be a new model called Project.

Project pages are controlled to the affiliate organization where they have the most expressive freedom, while sections are maintained by the site-wide editors.

A project landing page has a different URL:

```
http://news21.com/projects/the_western_edge
```