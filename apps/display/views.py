import jingo
import simplejson as json
from copy import deepcopy
from django import http
from django.http import HttpResponse

from display.queries import reports, grab_facet_response, grab_operating_systems, grabber 

def hello_world(request):
    return HttpResponse('Hello World')

def report(request,_id):
    report=grabber('',_id)#['_source']
    report = report['_source']
    #print report['_source']
    data = {
        "id":_id,
        "app_name":report['application_name'],
        "app_version":report['application_version'],
        "platform_version":report['platform_version'],
        "app_locale":report['application_locale'],
        "platform_buildId":report['platform_buildid'],
        "system":report['system_info']['system'],
        "system_version":report['system_info']['version'],
        "service_pack":report['system_info']['service_pack'],
        "cpu":report['system_info']['processor'],
        "time_start":report['time_start'],
        "time_end":report['time_end'],
        "passed":report['tests_passed'],
        "failed":report['tests_failed'],
        "skipped":report['tests_skipped'],
        "report_type":report['report_type'],
    }

    return jingo.render(request, 'display/functional_report.html', data)


def reporter(request,report_type='all'):
    print report_type
    oses=["windows nt","mac", "linux"]
    locales = ['en-US', 'es-ES', 'fr', 'ja-JP-mac', 'zh-TW', 'de', 'ko', 'pl', 'da', 'it']
    foo=reports()
    foo.clear_filters()
 
    if report_type=='functional':
        print 'foo'
        foo.add_filter_term({"report_type": "firefox-functional"})
        print foo.filters
    if request.method =="POST":
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
