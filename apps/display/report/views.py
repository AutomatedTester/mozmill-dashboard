import jingo
from django.http import HttpResponse, HttpResponseForbidden

from display.models import Results, Addons, Updates, EnduranceResults, Iterations, CheckPoints

BYTE_IN_MB=1048576.0

def mb_convert(byte):
    return int(round(byte/BYTE_IN_MB))


def report(request,_id):
    report = Results.objects.get(pk=_id)
    data = {
        "id":_id,
        "app_name":report.application_name,
        "app_version":report.application_version,
        "platform_version":report.platform_version,
        "app_locale":report.application_locale,
        "platform_buildId":report.platform_buildid,
        "system":report.system_info.system,
        "system_version":report.system_info.version,
        "service_pack":report.system_info.service_pack,
        "cpu":report.system_info.processor,
        "time_start":report.time_start,
        "time_end":report.time_end,
        "passed":report.tests_passed,
        "failed":report.tests_failed,
        "skipped":report.tests_skipped,
        "report_type":report.report_type,
        "mozmill_version": report.mozmill_version,
        'results':[],
    }

    data['extensions'] = Addons.objects.filter(results=report, addon_type='extension')
    data['themes'] = Addons.objects.filter(results=report, addon_type='theme')
    data['plugins'] = Addons.objects.filter(results=report, addon_type='plugin')

    #Make sure that there are no stupid argument
    try:
        request.GET['status']
    except:
        pass
    else:
        if not request.GET['status'] in ['all','failed','passed','skipped']:
            return HttpResponseForbidden()

    if data['report_type']=='firefox-functional':
        return jingo.render(request, 'display/report/functional.html', data)
    elif data['report_type']=='firefox-update':
        return update(request,data,report)
    elif data['report_type']=='firefox-endurance':
        return endurance(request,data,report)
    else:
        return HttpResponse(data['report_type']+" report view not implemented ... yet")

def endurance(request, data, report):
    data['app_sourcestamp']=report.platform_repository + '/rev/' + report.platform_changeset

    data['delay']=report.endurance.delay
    data['iterations']=report.endurance.iterations
    data['restart']=report.endurance.restart

    results = EnduranceResults.objects.filter(endurance=report.endurance)

    data['testCount'] = results.count()

    data['checkpointCount']=0 
    for res in results:
        iterations = Iterations.objects.filter(endurance_results=res)
        for iteration in iterations:
            checkpoints = CheckPoints.objects.filter(iterations = iteration)
            data['checkpointCount'] += checkpoints.count()

    data['checkpointsPerTest']='https://github.com/highriseo/Mozmill-Dashboard-4.0/issues/7'

    iterations = Iterations.objects.filter(endurance_results=results)
    for stattype in ['allocated','mapped','explicit','resident']:
        try:
            mem_report=getattr(iterations[0].stats, stattype)
        except Exception:
            pass
        else:
            data[stattype]={}
            for stat in ['min_mem','max_mem','ave_mem']:
                data[stattype][stat]=int(round(getattr(mem_report, stat)/BYTE_IN_MB))

    data['memresult']={}
    for stattype in ['allocated','mapped','explicit','resident']:
        data['memresult'][stattype]=[]

    for res in results:
        iterations = Iterations.objects.filter(endurance_results=res)
        for iteration in iterations:
            checkpoints = CheckPoints.objects.filter(iterations=iteration)
            for checkpoint in checkpoints:
                for stattype in ['allocated','mapped','explicit','resident']:
                    try:
                        checkpoint[stattype]
                    except:
                        pass
                    else:
                        data['memresult'][stattype].append({
                            'memory':int(round(getattr(checkpoint, stattype)/BYTE_IN_MB)),
                            'testFile':results.test_file,
                            'testMethod':results.test_method,
                        })

    data['testresult']=[]
    for stattype in ['allocated','mapped','explicit','resident']:
        #See if this statype exists in the data (this assumes that if it exists in the first it will exist in all)
        try:
            getattr(results[0].stats, stattype)
        except Exception:
            continue
        else:
            #If so, create an array to be rendered and start adding to it
            series_object= {}
            series_object['points']=[]
            series_object['name']=stattype #This song and dance is to allow for a DRY template
            for test in results:
                series_object['points'].append({
                    'memory':int(round(getattr(test.stats, stattype).ave_mem/BYTE_IN_MB)),
                    'testFile':test.test_file,
                    'testMethod':test.test_method,
                })

            data['testresult'].append(series_object)


    data['testresult_table']={}
    data['testresult_table']['tests']=[]
    for result in results:
        for stattype in ['allocated','mapped','explicit','resident']:
            try:
                getattr(result.stats, stattype)
            except:
                continue
            else:
                data['testresult_table'][stattype]=True
                data['testresult_table']['tests'].append({
                    stattype:True,
                    'min':mb_convert(getattr(result.stats, stattype).min_mem),
                    'max':mb_convert(getattr(result.stats, stattype).max_mem),
                    'average':mb_convert(getattr(result.stats, stattype).ave_mem),
                    'testFile':result.test_file,
                    'testMethod':result.test_method,
                })

    return jingo.render(request, 'display/report/endurance.html', data)

def update(request,data,report):
    try:
        updates = Updates.objects.filter(result = report)[0:1].get()
        update=updates
    except Updates.DoesNotExist:
        data['update_results']=False
        return jingo.render(request, 'display/report/update.html', data)
    else:
        data['update_results']=True

    data['pre']=update.build_pre
    data['post']=update.build_post

    data['channel']=update.patch.channel
    data['url_mirror']=update.patch.url_mirror
    data['size']=update.patch.size
    data['download_duration']=update.patch.download_duration
    data['type']=update.patch.patch_type
    data['disabled_addons']=update.build_post.disabled_addons


    if update.success:
        data['pass_fail']='Pass'
    else:
        data['pass_fail']='Fail'

    if update.patch.is_complete:
        data['complete']='complete'
    else:
        data['complete']='partial'

    if update.fallback:
        data['fallback']='fallback'
    else:
        data['fallback']='direct'

    return jingo.render(request, 'display/report/update.html', data)
