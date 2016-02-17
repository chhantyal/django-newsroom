# Introduction #

Affiliates are organizations or partners.  The system needs to know what object was authored by who and what organization the object belonged to when it was published or created.

# Schema #

So a conventional schema might look like:

```
Affiliate 1------(n) Story (n) ------ (n) User
```

A story is linked to Affiliate and User.   A story is published by one organization but can have many authors.  We have also been debating with Affiliate is better name as Org, so far Affiliate has a little more abstract meaning so we're sticking with it.
Originally we foreign-keyed affiliate to profile like

```
Affiliate 1 ------ (n) Profile    [not this]
```

But realized that the user should be allowed to change organizations and that should not affect the published object.

```
class Affiliate(models.Model):
     title = CharField()
     location = CharField()
     ...

class Story(model.Model):
     ...
     authors = models.ManyToManyField(User)
     affiliate = models.ForeignKey(Affiliate)
```

# A request example #

So to get a list of stories published by a specific group or affiliate ...

```
GET /stories/affiliate/uc_berkeley
```

URL mapper to view

```
def story_index(request, affiliate_slug=None):
    ...
    if affiliate_slug:
        stories = Story.objects.filter( affiliate=Affiliate.objects.get(slug=affiliate_slug) )
```

# Independent Affiliates #

What happens when a person publishes a story as themselves or is not affiliated with an organization?   We accommodate this by creating an "Independent" affiliation.

### A request example ###