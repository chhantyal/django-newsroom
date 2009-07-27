from datetime import date
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from django.contrib.flatpages.models import FlatPage


from promos.forms import *
from promos.models import *

def promo_billboard_homepage(request):
    """
    Send ONLY the latest billboard to the homepage whose start date is less than or equal to today 
    """
    today = date.today()
    # billboards = PromoBillboard.objects.filter(start_date__lte=date.today()).order_by('?')[:1]
    billboards = PromoBillboard.objects.filter(start_date__lte=date.today()).order_by('-start_date')[:1]

    home1 = []
    home2 = []
    home3 = []
    flatpages = FlatPage.objects.all()
    for x in flatpages:
        if x.url == '/home1/':
            home1.append(x)
        elif x.url == '/home2/':
            home2.append(x)
        elif x.url == '/home3/':
            home3.append(x)

    return render_to_response(
            'promo_billboard_homepage.html',{
            'billboards': billboards,
            'home1': home1,
            'home2': home2,
            'home3': home3,
             },
              context_instance=RequestContext(request))
