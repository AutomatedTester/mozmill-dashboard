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

    results = Results.objects.filter(report_type = 'firefox-%' % test_type)
     

    #Adds filters based on get paramaters for elastic search
    filter_request(request, results, 'os', 'system', oses)
    filter_request(request, results, 'locale', 
                   'application_locale', locales)

    ##If the dates have been set by the request use them, otherwise use the default
    try:
        request.GET['from_date']
        request.GET['to_date']
    except KeyError:
        pass
    else:
        pass

    #data['from_date']=es_object.from_date
    #data['to_date']=es_object.to_date
    
    if top_fail_view:
        return render_top_fail(request, results,data)
    else:
        return render_reports_view(request, results, data)
        
def render_reports_view(request, results, data):
    data['reports'] = results.objects.values() 
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

        required_fields = ['application_id', 'mozmill_version', 'system_info',
                           'tests_passed', 'tests_failed', 'tests_skipped',
                           'time_start', 'time_end', 'report_type', 'report_type']

        for field in required_fields:
            if not doc.has_key(field):
                return HttpResponse("Unfortunately the field %s is missing" % field)

        FIREFOX_APP_ID = "{ec8030f7-c20a-464f-9b0e-13a3a9e97384}"

        print doc['application_id']
        if FIREFOX_APP_ID != doc['application_id']:
            return HttpResponse("Unfortunately the incorrect Application ID was supplied")

        try:
            del doc['_id']
            del doc['_rev']
        except:
            # we are only clearing so rough data so ok to ignore the exception
            pass
        
        def _real_or_none(field):
            if doc.has_key(field):
                return doc[field]
            else:
                return None
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
                          report_type=_real_or_none('report_type'), 
                          tests_repository = _real_or_none('tests_repository'),
                          tests_changeset = _real_or_none('tests_changeset'),
                          time_start = datetime.datetime.strptime(doc['time_start'], date_format),
                          application_changeset = _real_or_none('application_changeset'),
                          system_info=system_info,
                          platform_version = _real_or_none('platform_version'),
                          tests_passed = doc['tests_passed'],
                          application_repository = _real_or_none('application_repository'),
                          platform_changeset = _real_or_none('platform_changeset'),
                          platform_repository = _real_or_none('platform_repository'),
                          tests_failed = doc['tests_failed'],
                          time_end= datetime.datetime.strptime(doc['time_end'], date_format),
                          application_locale = _real_or_none('application_locale'),
                          platform_buildid = _real_or_none('platform_buildid'),
                          application_version = _real_or_none('application_version'),
                          tests_skipped = doc['tests_skipped'],
                          time_upload=datetime.datetime.strptime(doc['time_upload'], date_format),
                          application_name = _real_or_none('application_name'),
                          mozmill_version = _real_or_none('mozmill_version'),
                          report_version = _real_or_none('report_version'))
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

    return HttpResponse('Data has been stored')
