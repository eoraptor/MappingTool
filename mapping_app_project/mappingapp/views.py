from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    context = RequestContext(request)

    context_dict = {'boldmessage': "Bold"}

    return render_to_response('mappingapp/index.html', context_dict, context)


def search(response):
    return HttpResponse("Search Page<br>"
                        "<a href='/mappingapp/'>Home</a><br>"
                        "<a href='/mappingapp/results'>Results</a>")


def results(response):
    return HttpResponse("Results table<br>"
                        "<a href='/mappingapp/search'>Search</a><br>"
                        "<a href='/mappingapp/'>Home</a>")