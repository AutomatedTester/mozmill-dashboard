import jingo
import simplejson as json
from copy import deepcopy
from django import http
from django.http import HttpResponse, HttpResponseForbidden

from display.queries import reports, grab_facet_response, grab_operating_systems, grabber 
from display.utils import filter_request

##This is a function to deal with adding filters to elastic search in a less general way but without code duplication in the view code
#The name parameter is whatever mozmill decides to call it. the Key is what it is in the request object


def reporter(request,report_type='all'):
    oses=['all',"windows nt","mac", "linux"]
    locales = ['all','en-US', 'es-ES', 'fr', 'ja-JP-mac', 'zh-TW', 'de', 'ko', 'pl', 'da', 'it']
    foo=reports()
    foo.clear_filters()
 
    if report_type=='functional':
        foo.add_filter_term({"report_type": "firefox-functional"})
    elif report_type=='endurance':
        foo.add_filter_term({"report_type": "firefox-endurance"})
    elif report_type=='update':
        foo.add_filter_term({"report_type": "firefox-update"})

    #Adds filters based on get paramaters for elastic search
    filter_request(request,foo,'os','system',oses)
    filter_request(request,foo,'locale','application_locale',locales)

    ##If the dates have been set by the request use them, otherwise use the default
    try:
        request.GET['from_date']
        request.GET['to_date']
    except KeyError:
        pass
    else:
        foo.from_date=request.GET['from_date']
        foo.to_date=request.GET['to_date']

    data = {
        'reports':foo.return_reports(),
        'operating_systems':oses, 
        'locales':locales,
        'from_date':foo.from_date,
        'to_date':foo.to_date,
        'current_os':request.GET.get('os','all'),
        'current_locale':request.GET.get('locale','all'),
        'report_type': report_type
    }

    if report_type == 'all':
        return jingo.render(request, 'display/reports.html', data)
    elif report_type == 'functional':
        return jingo.render(request, 'display/reports.html', data)
    elif report_type == 'endurance':
        return HttpResponse("GAH NO ENDURACE")
    elif report_type == 'update':
        return update(request,data)

def update(request,data):
        return jingo.render(request, 'display/updateReports.html',data)



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
