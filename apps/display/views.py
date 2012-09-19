import jingo
import json
import datetime

from django.http import HttpResponse

from display.utils import filter_request
from django.views.decorators.csrf import csrf_exempt

from models import Results, SystemInfo, Addons, DetailedResults

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
        date_format = '%Y-%m-%dT%H:%M:%SZ' 
        doc = json.loads(request.body)
        # TODO(David) Add validation checks to doc so we dont put duff data in
        try:
            del doc['_id']
            del doc['_rev']
        except:
            # we are only clearing so rough data so ok to ignore the exception
            pass
        

        # Save the system info
        system_info = SystemInfo(hostname = doc['system_info']['hostname'],
                                 service_pack = doc['system_info']['service_pack'],
                                 system = doc['system_info']['system'],
                                 version = doc['system_info']['version'],
                                 bits = doc['system_info']['bits'],
                                 processor = doc['system_info']['processor'])
        system_info.save()

        # Save the results
        results = Results(results=doc, 
                          report_type=doc['report_type'], 
                          tests_repository = doc['tests_repository'],
                          tests_changeset = doc['tests_changeset'],
                          time_start = datetime.datetime.strptime(doc['time_start'], date_format),
                          application_changeset = doc['application_changeset'],
                          system_info=system_info,
                          platform_version = doc['platform_version'],
                          tests_passed = doc['tests_passed'],
                          application_repository = doc['application_repository'],
                          platform_changeset = doc['platform_changeset'],
                          platform_repository = doc['platform_repository'],
                          tests_failed = doc['tests_failed'],
                          time_end= datetime.datetime.strptime(doc['time_end'], date_format),
                          application_locale = doc['application_locale'],
                          platform_buildid = doc['platform_buildid'],
                          application_version = doc['application_version'],
                          tests_skipped = doc['tests_skipped'],
                          time_upload=datetime.datetime.strptime(doc['time_upload'], date_format),
                          application_name = doc['application_name'],
                          mozmill_version = doc['mozmill_version'],
                          report_version = doc['report_version'])
        results.save()
        
        for adds in doc['addons']:
            addon = Addons(name = adds['name'],
                          is_compatible = adds['isCompatible'],
                          version = adds['version'],
                          addon_type = adds['type'],
                          addon_id = adds['id'],
                          is_active = adds['isActive'],
                          results = results)
            addon.save()

        for res in doc['results']:
            desres = DetailedResults(passed_function = res['passed_function'],
                                    name = res['name'],
                                    filename = res['filename'],
                                    failed = res['failed'],
                                    passed = res['passed'],
                                    results = results)
            desres.save()

    return HttpResponse('Hello World')
