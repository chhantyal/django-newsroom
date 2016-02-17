# Introduction #

Much of this discussion begins with the question:

  1. Where will project landing pages live and how will they be rendered.

An affiliate domain may have one or more project landing pages or mini-sites with unique URLs or permalinks.
The word permalink is used to denote a URL that should never change and is a unique identifier for that project.  This leads to less confusion for others linking to the site and maximizes search engine ranking.

The project will have a permalink under either:

  * http://news21.com/projects/a_project_slug
  * http://foo.example.com/projects/a_project_slug

If the latter is used then the project resides under a different domain so the site field is required to render the full URL or permalink.


# Schema #

Project have one or more affiliates and a site.  Stories have one or more projects.
```
story (n) ---- (n) project (1) ----- (n) site
                     (n)
                      |
                      |  
                     (n)
                  affiliate
```
# Model #
```
class Project(models.Model):
    """
    A project is always related to an affiliate and relates to a page
    that defines a project's landing page.    """

    affiliate = models.ManyToManyField(Affiliate)    
    site = models.ForeignKey(Site)
    url = models.URLField(
            blank=True,
            verify_exists=False,
            help_text="Is the project a separate website? Provide the public URL if it has one.",)
    title = models.CharField(
                max_length=100,
                help_text='The title of the project. i.e. "The American Dream"')
    slug = models.SlugField(unique=True)
    summary = models.TextField(
                help_text='Provide a summary that can be used to describe the project.')

    activity_begins = models.DateField(
                        help_text="When does production begin for this project?")

    activity_ends = models.DateField(
                        help_text="When is all production forcasted to end for this project?")

    comment_status = models.CharField(
                        max_length=1,
                        help_text="How should comments be treated for stories related to this project?",
                        choices = COMMENT_STATUS_CHOICES,
                        default = COMMENT_STATUS_OPEN,)


class Page(models.Model):
    """
    A project landing page, similar to story pages but there are not 
    multiple pages.
    """
    project = models.ForeignKey(Project,unique=True)
    content = models.TextField(
                help_text='The landing page for the project.',)


```

## An Issues / Projects / Stories Approach ##

Let's not have sub-projects.  Let's have "Issues" which can aggregate projects.  Think of an Issue as the overarching "magazine publication" for an affiliate for a semester.

As a sub-section of issues, let's have "Projects" which can aggregate stories.

In my previous work, we used to have "special preports" which aggregated stories with a specific keyword between a certain date range.  The stories were just displayed on the projects page as a list, with title and description and link back to each story.  This "special report" page had a title and a description.  And an image.  (And a keyword property - similar to topic\_path - which was used to gather the stories).  Within each story there was a link back to the special report page as well.  This Special Report is analogous to a project.

I think if we start with this as a bare bones skeleton for projects we could use this as a starting point on which to build from.

I think a lot of how the project page is displayed will be dictated by the students and will be reflective of the project itself.