# Django Groups As Affiliates RFC #

There was some thought about using groups to define affiliates.  Affiliates is a django model and organizational structure, and groups (django model Group) is more of a permissions structure.  Should we integrate them somehow?   Would that make things more flexible if we use the power of the existing groups functionality?  How would it look?

Typically permissions are handled in Django using the Group application and there is a model defined as Group that looks like:

```
Group (N)------(N) User
```

If we used Group to handle both permissions and affiliation we might have:

Group examples:
  * "UC Berkeley" ~ affiliate/org type definition
  * "USC"
  * "Fellow" ~ more like a role-type definition
  * "Author"
  * "Coordinator"
  * "Editor"

Stories would be filtered by group to create indexes based on authored group.

## API examples ##

To get list of stories based on group ... :

Get users in bob's groups
```
users = User.objects.filter(
                     groups_in=User.objects.get(username="bob").groups.all() )
```

Get stories from users in bob's group
```
stories = Stories.objects.filter(author__in=users)
```

Story Manager example
```
class StoryManager(models.Manager):

    def filter_by(self, **kwargs):
    
        if kwargs['user']:
              return self.filter(user=kwargs['user'])
        
       if kwargs['group']:
             return self.filter( author__in = User.objects.filter(
                                               groups_in=kwargs['group'] ))
```

## Request example ##

```
GET /stories/group/uc_berkeley
```

(url mapper to view)

```
def story_index(request, group_slug=None):
        ...
        stories = Story.objects.filter_by(
                            group=Group.objects.get(slug=group_slug))
        ...
```
## BAD ##

You can filter based on affiliation or group ... so you could get a story index based on a role-type group.

There would be groups that only exist as organizations.

Just feels wrong.