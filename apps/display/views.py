import jingo
import simplejson as json
from copy import deepcopy
from django import http
from django.http import HttpResponse, HttpResponseForbidden

from display.queries import reports, Facets #, grab_facet_response, grab_operating_systems, grabber 
from display.utils import filter_request

##This is a function to deal with adding filters to elastic search in a less general way but without code duplication in the view code
#The name parameter is whatever mozmill decides to call it. the Key is what it is in the request object


def reporter(request,test_type='all',top_fail_view=False):
    oses=['all',"windows nt","mac", "linux"]
    locales = ['all','en-US', 'es-ES', 'fr', 'ja-JP-mac', 'zh-TW', 'de', 'ko', 'pl', 'da', 'it']
    data = {
        'current_os':request.GET.get('os','all'),
        'current_locale':request.GET.get('locale','all'),
        'report_type': test_type,
        'operating_systems':oses, 
        'locales':locales,
    }
     
    #queries.Facets and queries.reports have been designed to be polymorphic   
    if top_fail_view:
        es_object=Facets()
    else:
        es_object=reports()
    
    es_object.clear_filters()
 
    if test_type=='functional':
        es_object.add_filter_term({"report_type": "firefox-functional"})
    elif test_type=='endurance':
        es_object.add_filter_term({"report_type": "firefox-endurance"})
    elif test_type=='update':
        es_object.add_filter_term({"report_type": "firefox-update"})

    #Adds filters based on get paramaters for elastic search
    filter_request(request,es_object,'os','system',oses)
    filter_request(request,es_object,'locale','application_locale',locales)

    ##If the dates have been set by the request use them, otherwise use the default
    try:
        request.GET['from_date']
        request.GET['to_date']
    except KeyError:
        pass
    else:
        es_object.from_date=request.GET['from_date']
        es_object.to_date=request.GET['to_date']
        
    data['from_date']=es_object.from_date,
    data['to_date']=es_object.to_date,


    if top_fail_view:
        return render_top_fail(request,es_object,data)
    else:
        return render_reports_view(request,es_object,data)
        
def render_reports_view(reqest,es_object,data):
    data['reports']=es_object.return_reports(),

    if test_type == 'all':
        return jingo.render(request, 'display/reports.html', data)
    elif test_type == 'functional':
        return jingo.render(request, 'display/reports.html', data)
    elif test_type == 'endurance':
        return jingo.render(request, 'display/reports.html', data)
    elif report_type == 'update':
        return update(request,data)



def render_top_fail(request,es_object, data):
    return HttpResponse("Top Fail!")
    
    



def top_fail(request):
    data = {}
    
    

    query = {
    'query':{
        'match_all':{}
    },
    'facets':{
        'tag':{
            "terms":{
                "field":"failed_function",
                "size":10
            }
        }
    }
}

    os_query = {
    'query':{
        'match_all':{}
    },
    'facets':{
        'tag':{
            "terms":{
                "script_field":"failed_function",
                "size":10
            }
        }
    }
}
    os_query=deepcopy(query)
    os_query['facets']['tag']['terms']['field']='system'
    oses = grab_operating_systems(os_query)

    if request.method=="POST":
        if request.POST['os'] in oses:
            query['query']={"term":{
                "system":request.POST['os']
                }
            }

    fails = grab_facet_response(query)
    data = {'fails':fails,'operating_systems':oses}
    return jingo.render(request, 'display/filtered_table.html', data)
