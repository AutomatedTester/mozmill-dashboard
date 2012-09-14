import jingo
import json
import datetime

from django.http import HttpResponse

from display.utils import filter_request
from django.views.decorators.csrf import csrf_exempt

from models import Results

##This is a function to deal with adding filters to elastic search in a less general way but without code duplication in the view code
#The name parameter is whatever mozmill decides to call it. the Key is what it is in the request object


def reporter(request, test_type='all', top_fail_view=False):
    #This needs to be dynamic. Unfortunately, performance is aweful if it is queried directly 
    #from elastic search. A cron job to get the result and cache it in the database is probably 
    #the right way to go.
    oses=['all',"windows nt","mac", "linux"]
    locales = ['all','en-US', 'es-ES', 'fr', 'ja-JP-mac', 'zh-TW', 'de', 'ko', 'pl', 'da', 'it']
    data = {
        'current_os':request.GET.get('os','all'),
        'current_locale':request.GET.get('locale','all'),
        'report_type': test_type,
        'operating_systems':oses, 
        'locales':locales,
    }

    results = Results
     
    #queries.Facets and queries.reports have been designed to be polymorphic   
    

    # es_object.add_filter_term({"report_type": "firefox-%s"%test_type})


    #Adds filters based on get paramaters for elastic search
    filter_request(request, results,'os','system',oses)
    filter_request(request, results,'locale','application_locale',locales)

    ##If the dates have been set by the request use them, otherwise use the default
    try:
        request.GET['from_date']
        request.GET['to_date']
    except KeyError:
        pass
    else:
        #es_object.from_date=request.GET['from_date']
        #es_object.to_date=request.GET['to_date']
        pass

    #data['from_date']=es_object.from_date
    #data['to_date']=es_object.to_date
    
    if top_fail_view:
        return render_top_fail(request, results,data)
    else:
        return render_reports_view(request, results, data)
        
def render_reports_view(request, results, data):
    data['reports']= results.objects.values() 
    test_type=data['report_type']

    if test_type == 'all':
        return jingo.render(request, 'display/reports/reports.html', data)
    elif test_type == 'functional':
        return jingo.render(request, 'display/reports/reports.html', data)
    elif test_type == 'endurance':
        return jingo.render(request, 'display/reports/updateReports.html', data)
    elif test_type == 'update':
        return jingo.render(request, 'display/reports/updateReports.html', data)

def render_top_fail(request, results, data):
    print results.objects.values()[:10]
    data['topfails']=results.objects.values()[:10]
    return jingo.render(request, 'display/facets/all.html', data)


@csrf_exempt
def report(request):
    if request.method=="POST":
        
        doc = json.loads(request.body)
        
        try:
            del doc['_id']
            del doc['_rev']
        except:
            # we are only clearing so rough data so ok to ignore the exception
            pass

        for counter, function in enumerate(doc['results']):
            if function['failed'] == 0:
                doc['results'][counter]['passed_function'] = function['name']
            else:
                doc['results'][counter]['failed_function'] = function['name']

        results = Results(results=doc, 
                          report_type=doc['report_type'], 
                          time_upload=datetime.datetime.strptime(doc['time_upload'], '%Y-%m-%dT%H:%M:%SZ'))
        results.save()


    return HttpResponse('Hello World')
