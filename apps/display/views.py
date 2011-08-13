import jingo
import simplejson as json
from copy import deepcopy
from django import http
from django.http import HttpResponse, HttpResponseForbidden

from display.queries import reports, grab_facet_response, grab_operating_systems, grabber 

def hello_world(request):
    return HttpResponse('Hello World')

def parse_results(tests,filter_value):
    results = []
    for test in tests:
        result = {}
        result['test']=test['name']
        result['filename']=test['filename']

        #the following is an algorithm to parse out the status and information field. It also filters the results. Good luck.
        if (test['failed']>0) and (filter_value in ['failed','all']):
            result['status']='failed'
            print result['status']
            result['information'] = test['fails'][0]['exception']['message']
            results.append(result)
            continue

        try:
            test['skipped']
        except:
            pass
        else:
            result['status']='skipped'
            result['information'] = test['skipped_reason']
            if filter_value in ['skipped','all']:
                results.append(result)
            continue

        #make sure that we have the right amount of passes and failes and make sure that there is a filter that allows for passes
        if (test['failed']==0) and (test['passed']>=0) and (filter_value in ['passed','all']):
            result['status']='passed'
            results.append(result)
            continue
    return results

def report(request,_id):
    report=grabber('',_id)
    report = report['_source']
    results = []
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
        'results':[],
    }


    #Figure out weather we should filter for all, failed, passed or skipped
    try:
        request.GET['status']
    except KeyError:
        data['status']='failed'
    else:
        if not request.GET['status'] in ['all','failed','passed','skipped']:
            return HttpResponseForbidden()
        data['status']=request.GET['status']

    data['results'] = parse_results(report['results'],data['status'])

    return jingo.render(request, 'display/report/functional.html', data)


##This is a function to deal with adding filters to elastic search in a less general way but without code duplication in the view code
#The name parameter is whatever mozmill decides to call it. the Key is what it is in the request object
def filter_request(request,foo,key,name,options):
    #foo
    try:
        request.GET[key]
    except:
        foo='bar'
        return

    if request.GET[key]=='all':
		return

    if request.GET[key] in options:
        foo.add_filter_term({name:request.GET[key]})
    else:
		raise



def reporter(request,report_type='all'):
    oses=['all',"windows nt","mac", "linux"]
    locales = ['all','en-US', 'es-ES', 'fr', 'ja-JP-mac', 'zh-TW', 'de', 'ko', 'pl', 'da', 'it']
    foo=reports()
    foo.clear_filters()
 
    if report_type=='functional':
        foo.add_filter_term({"report_type": "firefox-functional"})
    elif report_type=='endurance':
        foo.add_filter_term({"report_type": "firefox-endurance"})
    elif report_type=='updade':
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
