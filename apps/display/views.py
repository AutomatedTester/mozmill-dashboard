import jingo
import json
import datetime

from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from models import Results, SystemInfo, Addons, DetailedResults
from models import Iterations, Stats, StatsInfo, CheckPoints, Endurance, EnduranceResults
from models import Updates, BuildInfo, Patch

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

    if test_type == 'all':
        results = Results.objects.all().order_by('-time_start')
    else:
        results = Results.objects.filter(report_type = 'firefox-%s' % (test_type))
        
    try:
        os_query = request.GET['os']
        if os_query != 'all':
            results = results.filter(system_info__system__exact=os_query)
    except Exception as e:
        pass

    try:
        locale_query = request.GET['locale']
        if locale_query != 'all':
            results = results.filter(application_locale = locale_query)
    except Exception as e:
        pass
    
    ##If the dates have been set by the request use them, otherwise use the default
    try:
        from_date = request.GET['from_date']
        results = results.filter(time_start__gte = datetime.datetime(*[int(its) for its in from_date.split('-')]))
        to_date = request.GET['to_date']
        results = results.filter(time_start__lte = datetime.datetime(*[int(its) for its in to_date.split('-')]))
    except Exception as e:
        pass

    #data['from_date']=es_object.from_date
    #data['to_date']=es_object.to_date
    
    if top_fail_view:
        return render_top_fail(request, results[:100], data)
    else:
        return render_reports_view(request, results[:100], data)
        
def render_reports_view(request, results, data):
    data['reports'] = results 
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
        
        endurance = None
        if doc['report_type'] == 'firefox-endurance':

            endurance = Endurance(delay = doc['endurance']['delay'],
                                  entities = doc['endurance']['entities'],
                                  iterations = doc['endurance']['iterations'],
                                  restart = doc['endurance']['restart'])
            endurance.save()
            for res in doc['endurance']['results']:
                 
                stats_info_res = StatsInfo(max_mem = res['stats']['resident']['max'],
                                           ave_mem = res['stats']['resident']['average'],
                                           min_mem = res['stats']['resident']['min'])
                stats_info_res.save()
                stats_info_exp = StatsInfo(max_mem = res['stats']['explicit']['max'],
                                           ave_mem = res['stats']['explicit']['average'],
                                           min_mem = res['stats']['explicit']['min'])
                stats_info_exp.save()
                
                #Save Stats
                stats = Stats(resident = stats_info_res,
                              explicit = stats_info_exp)
                stats.save()
                endurance_results = EnduranceResults(test_method = res['testMethod'],
                                                     test_file = res['testFile'],
                                                     endurance = endurance,
                                                     stats = stats)
                endurance_results.save()


                for its in res['iterations']:
                    # Save The specific info for the stats
                    stats_info_res = StatsInfo(max_mem = its['stats']['resident']['max'],
                                           ave_mem = its['stats']['resident']['average'],
                                           min_mem = its['stats']['resident']['min'])
                    stats_info_res.save()
                    stats_info_exp = StatsInfo(max_mem = its['stats']['explicit']['max'],
                                           ave_mem = its['stats']['explicit']['average'],
                                           min_mem = its['stats']['explicit']['min'])
                    stats_info_exp.save()
                
                    #Save Stats
                    stats = Stats(resident = stats_info_res,
                              explicit = stats_info_exp)
                    stats.save()

                    iteration = Iterations(stats=stats,
                                           endurance_results = endurance_results)
                    iteration.save()

                    for checks in its['checkpoints']:
                        checkpoint = CheckPoints(resident = checks['resident'],
                                             timestamp = datetime.datetime.strptime(checks['timestamp'],
                                             '%Y-%m-%dT%H:%M:%S.%fZ'),
                                             explicit = checks['explicit'],
                                             label = checks['label'],
                                             iterations = iteration)
                        checkpoint.save()
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
                          report_version = _real_or_none('report_version'),
                          endurance = endurance)
        results.save()
    
        if doc.has_key('addons'):

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
            function = res['passed_function'] if res.has_key('passed_function') else res['failed_function']
            desres = DetailedResults(function = function,
                                    name = res['name'],
                                    filename = res['filename'],
                                    failed = res['failed'],
                                    passed = res['passed'],
                                    results = results)
            desres.save()

        if doc['report_type'] == 'firefox-update':
            for update in doc['updates']:
                patch = Patch(url_mirror = update['patch']['url_mirror'],
                          build_id = update['patch']['buildid'],
                          download_duration = update['patch']['download_duration'],
                          patch_type = update['patch']['type'],
                          is_complete = update['patch']['is_complete'],
                          channel = update['patch']['channel'],
                          size = update['patch']['size'])
                patch.save()
                build_pre = BuildInfo(build_id = update['build_pre']['buildid'],
                                      locale = update['build_pre']['locale'],
                                      disabled_addons = update['build_pre']['disabled_addons'],
                                      version = update['build_pre']['version'],
                                      useragent = update['build_pre']['user_agent'],
                                      url_aus = update['build_pre']['url_aus'],
                                      )
                build_pre.save()
                build_post = BuildInfo(build_id = update['build_post']['buildid'],
                                      locale = update['build_post']['locale'],
                                      disabled_addons = update['build_post']['disabled_addons'],
                                      version = update['build_post']['version'],
                                      useragent = update['build_post']['user_agent'],
                                      url_aus = update['build_post']['url_aus'],
                                      )
                build_post.save()

                updates = Updates(build_pre = build_pre,
                                  build_post = build_post,
                                  result = results,
                                  success = update['success'],
                                  fallback = update['fallback'],
                                  target_buildid = update['target_buildid'],
                                  patch = patch)
                updates.save()


    return HttpResponse('Data has been stored')
