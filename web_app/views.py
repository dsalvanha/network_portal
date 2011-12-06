from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout
from web_app.networks.models import *

import search as s
import itertools

def home(request):
    #return render_to_response('home.html', locals())
    genes = Gene.objects.all()

    bicl_count = Bicluster.objects.count()
    sp_count = Species.objects.count()
    net_count = Network.objects.count()
    motif_count = Motif.objects.count()

    #return render_to_response('home.html', {}, context_instance=RequestContext(request))
    return render_to_response('home.html', locals())

def about(request):
    version = "0.0.1"
    return render_to_response('about.html', locals())

def contact(request):
    return render_to_response('contact.html', locals())

def search(request):
    if request.GET.has_key('q'):
        q = request.GET['q']
        results = s.search(q)
        bicluster_ids = []
        biclusters = []
        genes = []
        gene_functions = {}
        terms = []

        for result in results:
            print result.keys()
            print result['doc_type']
            if result['doc_type']=='BICLUSTER':
                biclusters.append(result)
                if 'bicluster_id' in result and result['bicluster_id'] not in bicluster_ids:
                    bicluster_ids.append(result['bicluster_id'])
            #elif result['doc_type']=='GENE':
            if result['doc_type']=='GENE':
                if ('gene_function_type' in result):
                    # create sorted list of functions per gene; 
                    # use if user wants to display Gene: Functions
                    functions = zip(result['gene_function_type'], result['gene_function_name'])
                    gene_functions[result['gene_name']] = functions
                    ret = sorted(gene_functions.items())
                    # create a list of unique functions found among the collection
                    # of genes queried by user
                    terms.append(result['gene_function_name'])
                    terms_list = list(itertools.chain.from_iterable(terms))
                    terms_lc = map(lambda x:x.lower(), terms_list)
                    unique = set(terms_lc)
                    unique = list(unique)
                    unique.sort()
                    # all gene results together
                    genes.append(result)
                else:
                    genes.append(result)
                        
    return render_to_response('search.html', locals())

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')
