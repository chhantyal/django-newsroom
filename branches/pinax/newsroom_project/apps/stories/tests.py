from django.contrib.auth.models import User
from django.contrib.auth.models import get_hexdigest
from django.contrib.gis.utils import add_postgis_srs
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.template.defaultfilters import slugify

from geotags.models import Point

from stories.models import Story, StoryIntegrityError
from stories.models import Page
from stories.models import RelatedContent
from stories.constants import STORY_STATUS_DRAFT, STORY_STATUS_PUBLISHED
from utils.helpers import user_objects_qs


def create_draft_story(headline=None, user=None):
    story = Story()
    story.headline = headline
    #normally slugify will be handled by the UI
    story.slug = slugify(story.headline)
    story.summary = "Like I said in the headline, this is a test story."
    story.status = STORY_STATUS_DRAFT
    story.save()
    story.sites = Site.objects.all()
    if user:
        story.authors.add(user)
    story.save()
    return story

def create_published_story(headline=None, user=None):
    story = Story()
    story.headline = headline
    #normally slugify will be handled by the UI
    story.slug = slugify(story.headline)
    story.summary = "Like I said in the headline, this is a published story."
    story.status = STORY_STATUS_PUBLISHED
    story.save()
    story.sites = Site.objects.all()
    if user:
        story.authors.add(user)
    story.save()
    return story

def create_page(story):
    page = Page()
    page.story = story
    page.content = "super page content"
    page.pagenum = 1
    page.save()
    return page
    
def create_user(username):
    user =  User.objects.create_user(username, username+"@mail.com", "secret")
    return user

class StoryTests(TestCase):
    
    def setUp(self):
        self.user = create_user("user")
        self.story_draft = create_draft_story(
                headline="draft story")
        self.story_draft_with_user = create_draft_story(
                headline="draft story with user",
                user=self.user)
 

    def test_user_objects_qs(self):
        user_stories = user_objects_qs(Story, self.user)
        self.assertEqual(user_stories.count(), 1)
        self.assertEqual(user_stories.all()[0], self.story_draft_with_user)
        
    def _verify_page_count(self,count,story=None,msg=""):
        s = story if story else self.story_draft
        self.failUnlessEqual(s.pages.count(),count,msg)

    def test_get_story_for_author(self):
        self.assertEqual(list(Story.objects.get_for_author(self.user)),
            list(Story.objects.filter(authors=self.user )))
    
    def test_create_story(self):
        #self.failUnlessEqual(self._page_count(1),"New stories should have exactly one page")
        self._verify_page_count(1,msg="New stories should have exactly one page")
        self.failUnlessEqual(self.story_draft.pages[0].pagenum,1,"First page should be 1")

    def test_story_token(self):
        TOKEN = get_hexdigest("md5", settings.SECRET_KEY, self.story_draft.slug)
        self.assertEqual(TOKEN, self.story_draft.token)
        
    def test_story_always_has_one_or_more_pages(self):
        p1 = self.story_draft.pages[0]
        self.assertRaises(StoryIntegrityError,p1.delete)
        
    def test_story_add_page(self):
        new_page = self.story_draft.add_page()
        self.failUnlessEqual(new_page.pagenum,2,"This should be the second page for the story")
        self._verify_page_count(2,msg="This Story should have 2 pages")
        
    def test_add_remove_pages(self):
        p1 = self.story_draft.page_one
        p2,p3,p4 = [self.story_draft.add_page() for i in range(3)]

        self._verify_page_count(4,msg="This Story should have 4 pages")
        self.failUnlessEqual(p2.pagenum,2,"This should be Page 2")
        self.failUnlessEqual(p3.pagenum,3,"This should be Page 3")
        self.failUnlessEqual(p4.pagenum,4,"This should be Page 4")        
        
        p3.delete()
        
        #The live instances don't know that their page order has been updated
        # so we have to "refresh" them
        p4 = self.story_draft.pages[2]
        self._verify_page_count(3,msg="This Story should have 3 pages")
        self.failUnlessEqual(p2.pagenum,2,"This should be Page 2")
        self.failUnlessEqual(p4.pagenum,3,"Page 4 should have become Page 3 after delete")
        
        p1.delete()
        
        p2 = self.story_draft.pages[0]
        p4 = self.story_draft.pages[1]
        self._verify_page_count(2,msg="This Story should have 2 pages")
        self.failUnlessEqual(p2.pagenum,1,"Page 2 should have become Page 1 after delete")
        self.failUnlessEqual(p4.pagenum,2,"Page 3 should have become Page 2 after delete")
        
        p2.delete()
        
        p4 = self.story_draft.pages[0]
        self._verify_page_count(1,msg="This Story should have 1 page")
        self.failUnlessEqual(p4.pagenum,1,"Page 2 should have become Page 1 after delete")
        self.failUnlessEqual(self.story_draft.page_one,p4,"Original Page 4 should be the Page 1")
        self.assertRaises(StoryIntegrityError,p4.delete)

class RelatedContentTests(TestCase):

    def setUp(self):
        self.story_draft = create_draft_story(
                headline="draft story")

    def test_get_relatedcontent_empty(self):
        """
        Test get_related content when there is no related
        content
        """
        self.assertEqual(self.story_draft.get_relatedcontent(), {})

    def test_get_relatedcontent(self):
        """
        Test get_relatedcontent when some objects are
        associated with the
        """
        site = Site.objects.all()[0]
        RelatedContent(story=self.story_draft,
            object=site).save()
        self.assertEqual(self.story_draft.get_relatedcontent(),
            {"site":[site]})


            
class StoryUrlNewsroomTests(TestCase):
    """
    These tests exercise the views.
    """
    def setUp(self):
        self.user = create_user("user")
        self.other_user = create_user("other_user")
        self.story_draft = create_draft_story(
                headline="draft story")
        self.story_published = create_published_story(
                headline="published story")
        self.story_draft_with_user = create_draft_story(
                headline="draft story with user",
                user=self.user)
        self.story_draft_with_other_user = create_draft_story(
                headline="draft story with other user",
                user=self.other_user)
        self.page_with_user = create_page(story=self.story_draft_with_user)
        self.client.login(username="user", password="secret")
    def tearDown(self):
        self.client.logout()

    # TODO add test with multiple users
    def test_story_list_get_url(self):
        self.response = self.client.get(reverse("stories_story_list"))
        self.assertEqual(self.response.status_code, 200)

    def test_edit_story(self):
        self.response = self.client.get(
            reverse("stories_edit_story",
                kwargs={"story_id":self.story_draft_with_user.id}))
        self.assertEqual(self.response.status_code, 200)
        self.response = self.client.post(
            reverse("stories_edit_story",
                kwargs={"story_id":self.story_draft_with_user.id}),
            {"headline" : "test story",
             "summary" : "this story is a modifed test",
             "authors" : (self.user.id,),
             "sites" : (1,),
             "status":'D',
            })
        self.assertEqual(self.response.status_code, 302)

    def test_story_pages(self):
        self.response = self.client.get(reverse("stories_story_pages",
            kwargs={"story_id":self.story_draft_with_user.id}))
        self.assertEqual(self.response.status_code, 200)

    def test_story_media(self):
        self.response = self.client.get(reverse("stories_story_media",
            kwargs={"story_id":self.story_draft_with_user.id}))
        self.assertEqual(self.response.status_code, 200)

    def test_story_add_page(self):
        self.assertEqual(2, self.story_draft_with_user.page_set.count())
        self.response = self.client.get(reverse("stories_add_page",
            kwargs={"story_id":self.story_draft_with_user.id}))
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(3, self.story_draft_with_user.page_set.count())

    def test_story_edit_page(self):
        self.response = self.client.get(reverse("stories_edit_page",
            kwargs={"page_id":self.page_with_user.id}))
        self.assertEqual(self.response.status_code, 200)
        self.response = self.client.post(reverse("stories_edit_page",
            kwargs={"page_id":self.page_with_user.id}),
            {"content":"content of the page",
            "pagenum":1})
        self.assertEqual(self.response.status_code, 302)

    def test_save_page(self):
        self.response = self.client.get(reverse("stories_save_page",
            kwargs={"story_id":self.story_draft_with_user.id}))
        self.assertEqual(self.response.status_code, 200)

    def test_add_story(self):
        self.response = self.client.get(reverse("stories_add_story"))
        self.assertEqual(self.response.status_code, 200)
        self.response = self.client.post(reverse("stories_add_story"),
            {"headline" : "test story",
             "summary" : "this story is a test",
             "authors" : (self.user.id,),
             "sites" : (1,),
             "status":'D',
            })
        self.assertEqual(self.response.status_code, 302)

    def test_add_point_post_url(self):
        add_postgis_srs(900913)
        self.assertEqual(0, Point.objects.count())
        self.response = self.client.post(reverse('stories_story_add_edit_point',
            kwargs={"story_id" : self.story_draft_with_user.id}),
            {"point" : "SRID=900913;POINT(-13161849.549963182 4036247.7234083386)"})
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(1, Point.objects.count())
        self.assertEqual(self.story_draft_with_user, Point.objects.all()[0].object)


class StoryUrlPublicationTests(TestCase):
    """
    These tests exercise the publication views.
    """
    def setUp(self):

        self.user = create_user("user")
        self.other_user = create_user("other_user")
        self.story_draft = create_draft_story(
                headline="draft story")
        self.story_draft.add_page()
        self.story_published = create_published_story(
                headline="published story")
        self.story_published.add_page()

        self.story_draft_with_user = create_draft_story(
                headline="draft story with user",
                user=self.user)
        self.story_draft_with_user.add_page()
        self.story_draft_with_other_user = create_draft_story(
                headline="draft story with other user",
                user=self.other_user)
        self.story_draft_with_other_user.add_page()
        self.page_with_user = create_page(story=self.story_draft_with_user)
        self.client.login(username="user", password="secret")
        

    def tearDown(self):
        pass

    def test_story_list(self):
        """
        Test /stories/
        """
        self.response = self.client.get(
            reverse("stories_story_list_pub",
                    kwargs = {}))
        self.assertEqual(self.response.status_code, 200)

    def test_story_preview(self):
        """
        Test /stories/preview/<id>/<token>/
        """
        self.response = self.client.get(
            reverse("stories_story_preview_pub",
                    kwargs = {'story_id': self.story_draft.id,
                              'token': self.story_draft.token }))
        self.assertEqual(self.response.status_code, 301)


    def test_story_detail(self):
        """
        Test redirects for shortcut or outdated slug urls.
        """
        self.response = self.client.get(
            reverse("stories_story_detail_pub",
                    kwargs = {'story_id': self.story_draft.id,
                              'slug': self.story_draft.slug }))
        self.assertEqual(self.response.status_code, 301)

    def test_story_detail_no_slug(self):
        """
        Test /stories/<id>/
        """
        list_url = reverse('stories_story_list_pub')
        url = '%s%s/' % (list_url, self.story_draft.id)
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 301)

    def test_page_detail(self):
        self.response = self.client.get(
            reverse("stories_page_detail_pub",
                    kwargs = {'story_id': self.story_published.id,
                              'slug': self.story_published.slug,
                              'pagenum' : 1, }))
        self.assertEqual(self.response.status_code, 200)
        
    def test_page_detail_page2(self):
        self.response = self.client.get(
            reverse("stories_page_detail_pub",
                    kwargs = {'story_id': self.story_published.id,
                              'slug': self.story_published.slug,
                              'pagenum' : 2, }))
        self.assertEqual(self.response.status_code, 200)


    def test_page_detail_fix_url(self):
        self.response = self.client.get(
            reverse("stories_page_detail_pub",
                    kwargs = {'story_id': self.story_published.id,
                              'slug': 'just-made-this-up',
                              'pagenum': 1, }))
        self.assertEqual(self.response.status_code, 301)

    def test_page_detail_not_published(self):
        self.response = self.client.get(
            reverse("stories_page_detail_pub",
                    kwargs = {'story_id': self.story_draft.id,
                              'slug': self.story_draft.slug,
                              'pagenum' : 1, }))
        self.assertEqual(self.response.status_code, 404)

    def test_page_detail_not_on_site(self):
        self.story_published.sites = []
        self.story_published.save()
        self.response = self.client.get(
            reverse("stories_page_detail_pub",
                    kwargs = {'story_id': self.story_published.id,
                              'slug': self.story_published.slug,
                              'pagenum' : 1, }))
        self.assertEqual(self.response.status_code, 404)

    def test_page_detail_preview(self):
        self.response = self.client.get(
            reverse("stories_page_preview_pub",
                    kwargs = {'story_id': self.story_draft.id,
                              'slug': self.story_draft.slug,
                              'pagenum' : 1, 
                              'token': self.story_draft.token }))
        self.assertEqual(self.response.status_code, 200)





