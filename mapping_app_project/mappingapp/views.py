from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
#from multiuploader.forms import MultiUploadForm

def index(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('mappingapp/index.html', context_dict, context)



def search(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('mappingapp/search.html', context_dict, context)



def results(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('mappingapp/results.html', context_dict, context)



def upload(request):
    context = {'uploadForm': MultiUploadForm()}

    return render_to_response('mappingapp/upload.html', context=context)



def edit(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('mappingapp/edit.html', context_dict, context)

