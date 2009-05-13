from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from promos.models import Promo 
from promos.forms import PromoForm
from promos.models import PromoImage
from promos.models import PromoLink
from django.contrib.auth.models import User

from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from django.forms.models import inlineformset_factory

if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail


def front(request):
    return render_to_response(
              'promos/front.html',
              {},
              context_instance=RequestContext(request))

def promo_add(request):
    """
    Process a new promo submission.
    """

    if request.method == "POST":
        form = PromoForm(request.POST)
        if form.is_valid():
            promo = form.save(commit=False)
            promo.submitter = request.user
            promo.save()
            to_user = [mail_tuple[1] for mail_tuple in settings.PROMO_MODERATORS]
            message = render_to_string('promos/promo_sent.txt', { 'user': request.user , 'current_site': Site.objects.get_current().domain, 'object': promo.id })
            send_mail("promo_submitted", message, settings.DEFAULT_FROM_EMAIL, to_user)
            request.user.message_set.create(
                message='Your promo has been submitted.')

            return HttpResponseRedirect(reverse('promos_promo_list'))

    else:
        form = PromoForm()

    return render_to_response(
              'promos/promo_add.html',
              {'form':form},
              context_instance=RequestContext(request))

def promo_edit(request, id):
    """
    Edit an existing promo.
    """
    promo = get_object_or_404(Promo, pk=id)

    PromoImageInlineFormSet = inlineformset_factory(Promo, PromoImage)   
    if request.method == "POST":
        formset = PromoImageInlineFormSet(request.POST, request.FILES, instance=promo)
        form = PromoForm(request.POST, instance=promo)
        if formset.is_valid():
            formset.save()
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your promo has been edited.')
            return HttpResponseRedirect(reverse('promos_promo_list'))
    else:
        formset = PromoImageInlineFormSet(instance=promo)
        form = PromoForm(instance=promo)        

    return render_to_response(
              'promos/promo_edit.html',
              ({'form': form, 'formset': formset}),
              context_instance=RequestContext(request))

def promo_list(request):
    """
    Get index of promos.
    """

    promos = Promo.objects.all()
    promo_image = PromoImage.objects.all()

    return render_to_response(
                'promos/promo_list.html',{
                'promos': promos,
                'promo_image': promo_image,
                },
              context_instance=RequestContext(request))

def promo_detail(request, id):
    """
    Get promo details.
    """
    promo = Promo.objects.get(pk=id)
    # do not use this: promo_link = promo.promolink_set.all() - a pain for introspection.
    promo_link = PromoLink.objects.filter(promo=id)
    promo_image = PromoImage.objects.filter(promo=id)

    return render_to_response(
              'promos/promo_detail.html',{
              'promo': promo,
              'promo_link': promo_link,
              'promo_image': promo_image,
             },
              context_instance=RequestContext(request))

