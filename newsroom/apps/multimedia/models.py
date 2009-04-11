from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField

from multimedia.constants import MEDIA_TYPES, MEDIA_STATUS_CHOICES, MEDIA_STATUS_DRAFT
from utils.model_inheritance import ParentModel,ChildManager
from videos.models import Video as NativeVideoModel

class MediaBase(ModelBase):
    def __init__(cls, name, bases, attrs):
        """
        Registers the media types with the class. Media will
        have a list of all known media types in the media_types list attribute. Ex:
        
        In [1]: from multimedia.models import Media

        In [2]: Media.media_types
        Out[2]: ['Image', 'Video']
        
        Additionally, each subclass of Media will have a media_type attribute
        indicating the media type string registered with Media. By default this is just
        the class name, but it can be overridden by explicitly adding a media_type attribute
        to subclass definitions. Ex:
        
        class Test(Media):
            pass
            
        class Another(Media):
            media_type = 'another_media'
            
        >>> Media.media_types
        ['Test','another_media']
        
        >>> t = Test()
        >>> t.media_type
        'Test'
        """
        #TODO: media_type doesn't work for Media instances (subclasses OK)
        
        if not hasattr(cls,'media_types'):
            cls.media_types = []
        else:
            if hasattr(cls,'media_type'):
                cls.media_types.append(cls.media_type)
            else:
                setattr(cls,'media_type',name)
                cls.media_types.append(name)
    
#class MediaAttribute(object):
#    """
#    A descriptor that allows Media properties to look for the
#    property name on the underlying content object (the generic relation)
#    If the content object contains the attribute, return it from there, otherwise
#    return from the Media instance
#    """
#    def __init__(self,**kwargs):
#        self.name = kwargs.get('fn')
#        self.attrname = kwargs.get('syn',self.name)
#    
#    def __get__(self,obj,type=None):
#        if hasattr(obj.media_item,self.name):
#            return getattr(obj.media_item,self.name)
#        else:
#            return getattr(obj,'m_%s'%self.attrname)
#    
#    def __set__(self,obj,value):
#        if hasattr(obj.content_object,self.name):
#            obj.media_item.__dict__[self.name] = value
#        else:
#            obj.__dict__['m_%s'%self.attrname] = value
    
    
class Media(ParentModel):
    """
    A generic container for media items.
    
    
    """
    __metaclass__ = MediaBase
    
    #owner = models.ForeignKey(User)
    site = models.ForeignKey(Site)
    authors = models.ManyToManyField(User)
    title = models.CharField(max_length=128,blank=True)
    summary = models.TextField(blank=True)
    attribution = models.TextField(blank=True)
    tags = TagField()
    status = models.CharField(
                        max_length=1,
                        choices=MEDIA_STATUS_CHOICES,
                        default=MEDIA_STATUS_DRAFT,
                        help_text=_(u'Only published items will appear on the site.'),)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    media_item = generic.GenericForeignKey('content_type', 'object_id')
    
    #def __unicode__(self):
    #    """
    #    experimental: output self as HTML ala Django Forms
    #    so that template authors can do things like
    #    {{some_instance.media}}
    #    """
    #    pass
        
    objects = models.Manager()
    children = ChildManager()
    
    class Meta:
        verbose_name_plural = 'Media'
    
    def __unicode__(self):
        return self.title
        
    @property
    def authors(self):
        """
        Returns a comma separated string of the author names
        """
        #TODO: format first/last if exists
        return ",".join([user.username for user in self.owners.all()])
    
    def get_insert_snippet(self):
        """
        Creates the text snippet that Story authors will paste into their content to indicate that the
        media item should render should render itself there.
        
        The most basic form of the tag will look like
        
            {% media_insert <media_id> %}
            
        where media_id is the id of a Media object.
        
        If the user supplied a title with the media item, we tack that in as a convenience so that authors
        can quickly identify which media item will be shown when they are editing stories.
        An example snippet might then look like:
            
            {% media_insert 364 "obama speaking" %}
        
        Individual media types may desire/require arbitrary parameters for initializing/customizing the media
        object. Media subclasses should override this method so that they can translate additional arguments
        into the snippet in a way that the render method will be able to leverage.
        """
        if len(self.title):
            return '{%% media_insert %d "%s" %%}' % (self.id,self.title,)
        else:
            return "{%% media_insert %d %%}" % self.id
    
    def get_parent_model(self):
        return Media

class Image(Media):
    """
    A Media container for Photologue Photo instances
    """
    pass
    
    
class Video(Media):
    """
    A Media container for Video instances
    """
    
    @staticmethod
    def associate(sender,**kwargs):
        """
        post_save signal handler that associates any new videos.Video instances with a multimedia.Video instance
        """
        if kwargs.get('created',False):
            media_item = kwargs.get('instance')
            video = Video()
            video.media_item = media_item
            video.site = media_item.site
            video.title = media_item.title
            video.summary = media_item.summary
            video.tags = media_item.tag_list
            video.save()
            video.authors.add(media_item.authors.all())


post_save.connect(Video.associate,NativeVideoModel)   
        