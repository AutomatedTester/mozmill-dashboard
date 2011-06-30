import jingo
import simplejson as json
from copy import deepcopy
from django import http
from django.http import HttpResponse

from display.queries import reports, grab_facet_response, grab_operating_systems

def hello_world(request):
    return HttpResponse('Hello World')

def all_reports(request):
    oses=["windows nt","mac", "linux"]
    locales = ['en-US', 'es-ES', 'fr', 'ja-JP-mac', 'zh-TW', 'de', 'ko', 'pl', 'da', 'it']
    foo=reports()

    if request.method =="POST":
        foo.clear_filters()
        foo.from_date=request.POST['from_date']
        foo.to_date=request.POST['to_date']
        if request.POST['os'] in oses:
            foo.add_filter_term({'system':request.POST['os']})
        if request.POST['locale'] in locales:
            foo.add_filter_term({'application_locale':request.POST['locale']})

    data = {
        'reports':foo.return_reports(),
        'operating_systems':oses, 
        'locales':locales,
        'from_date':foo.from_date,
        'to_date':foo.to_date,
    }
    return jingo.render(request, 'display/reports.html', data)



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
    print json.dumps(os_query)
    os_query=deepcopy(query)
    os_query['facets']['tag']['terms']['field']='system'
    oses = grab_operating_systems(os_query)

    if request.method=="POST":
        print 'POST'
        if request.POST['os'] in oses:
            query['query']={"term":{
                "system":request.POST['os']
                }
            }

    fails = grab_facet_response(query)
    data = {'fails':fails,'operating_systems':oses}
    return jingo.render(request, 'display/filtered_table.html', data)
