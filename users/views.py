from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Personal


# Create your views here.

def index(request):
    user_objs = Personal.objects.order_by('-cid')[:5]
    template = loader.get_template('users/index.html')
    context = {
        'user_objs': user_objs,
    }
    return HttpResponse(template.render(context, request))

def user_info(request, cid):
    return HttpResponse("You're looking at the info for the user with cid %s." % cid)
