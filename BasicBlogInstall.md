# Basic Apps Blog #

http://code.google.com/p/django-basic-apps/

## Installation ##

To install this app,

1. create a folder named 'basic' under /newsroom/apps/ :
```
    mkdir apps/basic
```

2. Create an init.py file:
```
    touch apps/basic/__init__.py
```

3. cd /newsroom/apps/basic/
```
svn checkout http://django-basic-apps.googlecode.com/svn/trunk/blog blog
```

4. add 'basic.blog' to your project's INSTALLED\_APPS list in your settings.py file.

### Dependencies ###

5. Django Comments is likely already installed.  But to activate this for django newsroom add 'django.contrib.comments' to INSTALLED\_APPS.

For more info, see: http://www.djangoproject.com/documentation/add_ons/#comments

6. Django Tagging is likely already installed.  But to activate this for django newsroom add 'tagging' to INSTALLED\_APPS.

For more info, see: http://code.google.com/p/django-tagging Django Tagging

7. install basic.inlines

From within the apps/basic directory:
```
svn checkout http://django-basic-apps.googlecode.com/svn/trunk/inlines inlines
```

8. Add 'basic.inlines' to INSTALLED\_APPS.

9. Install Markup

Markup and Inlines requires Markdown be installed.  To do this, run the following commands from within your virtual env:

```
easy_install ElementTree
easy_install Markdown
```

Afterward, be sure to add 'markup' to your INSTALLED\_APPS setting

For more info, see: http://www.djangoproject.com/documentation/add_ons/#markup

## Getting Up and Running ##

10. Add the following urls to djangonewsroom's main urls.py:

```
(r'^blog/', include('basic.blog.urls')),
(r'^comments/', include('django.contrib.comments.urls')),
```

11. Override the the blog's templates by copying them from newsroom/apps/basic/blog/templates/blog into the newsroom/templates/blog folder.  Example:

```
cd working/trunk/newsroom/templates/
cp -r /Users/jetynan/dev/newsroom-env/working/trunk/newsroom/apps/basic/blog/templates/blog .
```

12. Run ./manage.py syncdb
You should see the following:

```
Creating table blog_categories
Creating table blog_posts
Creating table inline_types
Creating table django_comments
Creating table django_comment_flags
Installing index for blog.Post model
Installing index for inlines.InlineType model
Installing index for comments.Comment model
Installing index for comments.CommentFlag model
```