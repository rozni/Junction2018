from django.template import loader
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from . import coffee

def v1(request):

    context = None
    if request.POST:
        query = request.POST['query']
        context = dict(
            queried=True,
            query=query,
            results=coffee.search(query),
        )
    return render(request, 'front_end/v1.html', context)

def v2(request):

    context = None
    if request.POST:
        query = request.POST['query']
        context = dict(
            queried=True,
            query=query,
            results=coffee.search2(query),
        )
    return render(request, 'front_end/v2.html', context)
