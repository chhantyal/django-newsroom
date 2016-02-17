# Introduction #

We may want to set up a pub1.news21.com and pub2.news21.com to test/build the front facing django project/sites.

We may also want to create cms.news21.com to test the production cms.

We may also want to differentiate between this and what's happening on the dev server.

For the public facing sites, we should use the templates/css/js that ships with django-base.

Yet, these many sites would potentially be pulling from the same database.. based on the Sites.site attribute.

How do we minimize the duplication of code in the views?  If we use generic views then would the duplication be minimal?

We may want to do a little research in how people do it. Here are a few places to start.  Afterward, we can hone in and define the best way to implement this.

## mod\_wsgi and django ##

http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango

http://code.djangoproject.com/wiki/django_apache_and_mod_wsgi

http://www.technobabble.dk/2008/aug/25/django-mod-wsgi-perfect-match/

http://blog.davidziegler.net/post/88177012/deploying-a-pinax-project-with-mod-wsgi

http://effbot.org/zone/django-multihost.htm

http://blog.dougalmatthews.com/2008/08/running-multiple-websites-in-the-same-django-app/


## Sites.site and templates ##